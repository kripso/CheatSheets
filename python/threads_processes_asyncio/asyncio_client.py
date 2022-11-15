import asyncio
import time
import aiohttp
import random
from dataclasses import dataclass
from requests.exceptions import Timeout


@dataclass
class ClientResponse:
    passed: bool = None
    response: any = None
    status_code: int = None
    error: str = None

    def __post_init__(self):
        self.passed = True if self.error == None else False


class RetryTimeout(Timeout):
    def __init__(self, count: int):
        msg = f"Request Failed After {count} Retries"
        super().__init__(msg)


class Configuration:
    TIMEOUT = 6


def retry_on_timeout(num_of_retries=5):
    def _timeout_retry(func):
        async def _retry_function(*args, **kwargs):
            timeout = kwargs["timeout"]
            for _ in range(num_of_retries):
                kwargs["timeout"] = timeout
                try:
                    response = await func(*args, **kwargs)
                except aiohttp.ClientResponseError as err:
                    return ClientResponse(error=f"Client Response error: {err}")
                except asyncio.TimeoutError:
                    timeout += 1
                except BaseException as err:
                    return ClientResponse(error=f"Unknown error: {err}")
                else:
                    return response
            return ClientResponse(error=f"Timeout error")

        return _retry_function

    return _timeout_retry


class AsyncClient:
    def __init__(self, authorization):
        self.auth_header = authorization

    async def create_session(self):
        self.my_conn = aiohttp.TCPConnector(limit=100)
        self.session = aiohttp.ClientSession(connector=self.my_conn)

    async def close_session(self):
        await self.session.close()
        await self.my_conn.close()

    async def with_session(self, func):
        await self.create_session()
        result = await func()
        await self.close_session()

        return result

    @retry_on_timeout()
    async def request(self, method, path, data=None, json=None, accept="application/json", timeout=Configuration.TIMEOUT):
        kwargs = {
            "method": method,
            "url": path,
            "headers": {
                "authorization": self.auth_header,
                "content-type": "application/json",
                "accept": accept,
            },
            "timeout": timeout,
            "data": data,
            "json": json,
            "raise_for_status": True,
        }

        async with self.session.request(**kwargs) as r:
            return ClientResponse(response=await r.json(), status_code=r.status)

    def post(self, path, data=None, json=None, accept="application/json", timeout=Configuration.TIMEOUT):
        return self.request("POST", path, data, json, accept, timeout=timeout)

    def put(self, path, data=None, json=None, accept="application/json", timeout=Configuration.TIMEOUT):
        return self.request("PUT", path, data, json, accept, timeout=timeout)

    def get(self, path, data=None, json=None, accept="application/json", timeout=Configuration.TIMEOUT):
        return self.request("GET", path, data, json, accept, timeout=timeout)

    def delete(self, path, data=None, json=None, accept="application/json", timeout=Configuration.TIMEOUT):
        return self.request("DELETE", path, data, json, accept, timeout=timeout)


async def download_all(client, urls: list):
    tasks = []
    for index, url in enumerate(urls):
        payload = {"some": f"json_{index}"}
        task = asyncio.ensure_future(client.get(path=url, json=payload))
        tasks.append(task)
    return zip(urls, await asyncio.gather(*tasks, return_exceptions=True))


if __name__ == "__main__":
    url_list = [f"https://httpbin.org/delay/{random.randint(2,5)}" for _ in range(20)]
    client = AsyncClient("", "")

    start = time.time()
    futures = asyncio.run(client.with_session(lambda: download_all(client, url_list)))
    end = time.time()

    print(list(futures))
    print(f"download {len(url_list)} links in {end - start} seconds")
