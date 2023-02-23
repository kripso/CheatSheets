from playwright.async_api import async_playwright
from typing import List
import asyncio
import logging



async def record_tests(urls: List[str]):
    async with async_playwright() as playwright:
        browser_type = playwright.chromium
        browser = await browser_type.launch(headless=False)
        context = await browser.new_context(
            locale="en-US",
        )
        page = await context.browser.new_page()
        for url in urls:
            await page.goto(url)
            await page.get_by_role("button", name="Accept all").click()
            await page.pause()


def main():
    urls = ["https://www.google.com?&hl=en-US"]

    asyncio.run(record_tests(urls))


if __name__ == "__main__":
    main()
