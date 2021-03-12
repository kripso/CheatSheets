from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import pandas as pd


options = webdriver.ChromeOptions()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--allow-running-insecure-content')
options.add_argument('--headless')
options.add_argument("--window-size=1920,1080")
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')
options.add_argument('--ignore-certificate-errors')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
driver = webdriver.Chrome(executable_path='D:\Krips\Documents\Programing\python_exp\WebScraping\chromedriver.exe', chrome_options=options)

# driver = webdriver.Chrome('D:\Krips\Documents\Programing\python_exp\WebScraping\chromedriver.exe')

driver.get('https://www.amd.com/en/direct-buy/sk')
products = driver.find_elements_by_xpath('//div[@class="direct-buy"]')

rx6800xt = []
for div in range(len(products)):
    if 'AMD Radeon™ RX 6800 XT Graphics' in products[div].text:
        rx6800xt.append(products[div].text)

print(rx6800xt)
