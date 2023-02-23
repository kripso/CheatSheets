import asyncio
import aiohttp
import posixpath
from dataclasses import dataclass

# import nest_asyncio # only neceseary in jupyter notebooks
# nest_asyncio.apply()

RETRYABLE_ERROR_DESCRIPTIONS = ("Client Timeout Error", "Client Connector Error")


@dataclass
class ClientResponse:
    passed: bool = None
    redirected: bool = None
    response: dict = None
    error: str = None
    status_code: int = None

    def __post_init__(self):
        self.passed = True if self.error == None else False

        if self.passed:
            if 200 <= self.status_code < 300:
                self.redirected = False
            if 300 <= self.status_code < 400:
                self.redirected = True


def retry(func):
    async def _retry_function(*args, **kwargs):
        for _ in range(Configuration.ASYNC_RETRY_COUNT):
            try:
                response = await func(*args, **kwargs)
                if response.error != None and response.error.startswith(RETRYABLE_ERROR_DESCRIPTIONS):
                    await asyncio.sleep(Configuration.ASYNC_BACKOFF_FACTOR)
                    continue
            except BaseException as err:
                return ClientResponse(error=f"Unknown error: {err}")
            else:
                return response
        return ClientResponse(error=f"Client has reached the maximum number of {Configuration.ASYNC_RETRY_COUNT} retries")

    return _retry_function


class Configuration:
    # Request handling
    ASYNC_BACKOFF_FACTOR = 1
    ASYNC_RETRY_COUNT = 2
    ASYNC_TCP_LIMIT = 25
    ASYNC_TIMEOUT = aiohttp.ClientTimeout(
        total=None,  # if `None` wait for unlimited time or `sock_connect` and `sock_read`
        sock_connect=5,  # How long to wait before an open socket allowed to connect
        sock_read=5,  # How long to wait with no data being read before timing out
    )


class AsyncClient:
    REQUEST_KWARGS = {
        "timeout": Configuration.ASYNC_TIMEOUT,
        "data": None,
        "json": None,
        "content_type": "application/json",
        "accept": "application/json",
    }

    def __init__(self, authorization):
        self.auth_header = authorization

    async def create_session(self, limit):
        self.my_conn = aiohttp.TCPConnector(limit=limit)
        self.session = aiohttp.ClientSession(connector=self.my_conn)

    async def close_session(self):
        await self.session.close()
        await self.my_conn.close()

    async def with_session(self, limit: int = Configuration.ASYNC_TCP_LIMIT, func: any = None):
        await self.create_session(limit)
        result = await func()
        await self.close_session()

        return result

    @retry
    async def _request(self, method, path, **requested_kwargs):
        kwargs = {
            "method": method,
            "url": path,
            "headers": {
                "authorization": self.auth_header,
                "content-type": requested_kwargs["content_type"],
                "accept": requested_kwargs["accept"],
            },
            "timeout": requested_kwargs["timeout"],
            "data": requested_kwargs["data"],
            "json": requested_kwargs["json"],
            "raise_for_status": True,
        }
        try:
            async with self.session.request(**kwargs) as r:
                result = ClientResponse(response=await r.json(), status_code=r.status)
        except aiohttp.ClientResponseError as err:
            return ClientResponse(error=f"Client Response error: {err}")
        except aiohttp.ClientConnectorError as err:
            return ClientResponse(error=f"Client Connector Error: {err}")
        except aiohttp.ServerDisconnectedError as err:
            return ClientResponse(error=f"Server Disconnected Error: {err}")
        except asyncio.TimeoutError as err:
            return ClientResponse(error=f"Client Timeout Error: {err}")
        except BaseException as err:
            return ClientResponse(error=f"Unknown error: {err}")

        return result

    def post(self, path, **requested_kwargs):
        return self._request("POST", path, **(AsyncClient.REQUEST_KWARGS | requested_kwargs))

    def put(self, path, **requested_kwargs):
        return self._request("PUT", path, **(AsyncClient.REQUEST_KWARGS | requested_kwargs))

    def get(self, path, **requested_kwargs):
        return self._request("GET", path, **(AsyncClient.REQUEST_KWARGS | requested_kwargs))

    def delete(self, path, **requested_kwargs):
        return self._request("DELETE", path, **(AsyncClient.REQUEST_KWARGS | requested_kwargs))




if __name__ == "__main__":
    import time
    import random

    ASYNC_CHUNK_SIZE = 4

    async def download_all(urls: list):
        tasks = []
        for index, url in enumerate(urls):
            payload = {"some": f"json_{index}"}
            task = asyncio.ensure_future(client.get(path=url, json=payload))
            tasks.append(task)
        return await asyncio.gather(*tasks)

    url_list = [f"https://httpbin.org/delay/{3+random.choice([0,5])}" for _ in range(8)]
    print(url_list)
    client = AsyncClient("")

    start = time.time()
    futures = asyncio.run(client.with_session(ASYNC_CHUNK_SIZE, lambda: download_all(url_list)))
    end = time.time()

    print(futures)
    # print([future.status_code for future in futures])
    print(f"download {len(url_list)} links in {end - start} seconds")
