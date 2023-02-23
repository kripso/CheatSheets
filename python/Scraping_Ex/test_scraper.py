from DataManager import DataManager
from typing import List
from playwright.async_api import async_playwright
from PIL import Image
import requests
import asyncio
import random
import time
import io
import logging

data_manager = DataManager()


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
            # await page.get_by_role("button", name="Accept all").click()
            await page.pause()

        links = list(await page.query_selector_all(".b-photos__item"))
        results = []

        for tmp in links:
            await tmp.click()
            try:
                img = await page.wait_for_selector("#content > div.pswp.pswp--open.m-media.pswp--notouch.pswp--css_animation.pswp--svg.pswp--zoom-allowed.pswp--visible.pswp--animated-in.pswp--has_mouse > div.pswp__scroll-wrap > div.pswp__container > div:nth-child(2) > div > img", state="visible")
            except:
                pass
            await asyncio.sleep(0.5)
            await page.keyboard.press('Escape')
            results.append(asyncio.ensure_future(img.get_attribute("src")))

        return await asyncio.gather(*results)


def img_down(link, name):
    try:
        response = requests.get(link)
        content = response.content
        image_file = io.BytesIO(content)
        image = Image.open(image_file)
        data_manager.save_image(name, image)
    except BaseException as err:
        # logger.info(err)
        print(err)


def main():

    links = asyncio.run(record_tests(['https://google.com']))
    for image in links:
        time.sleep(1)
        img_down(image, 'ruzenka')


if __name__ == "__main__":
    main()
