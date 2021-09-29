import sys
from selenium import webdriver
import platform
import smtplib
from win10toast import ToastNotifier

# user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
browser = None
options = webdriver.ChromeOptions()

options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-gpu')
options.add_argument('--disable-dev-shm-usage')
options.add_argument("--window-size=1920,1080")
options.add_argument('--ignore-certificate-errors')
user_agent = 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36'
options.add_argument(f'user-agent={user_agent}')
options.add_argument('--allow-running-insecure-content')
options.add_argument(f'user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.50 Safari/537.36')

if (platform.system() == 'Windows'):
    browser = webdriver.Chrome(executable_path='D:\Krips\Documents\Programing\python_exp\WebScraping\chromedriver.exe', options=options)
else:
    browser = webdriver.Chrome('D:\Krips\Documents\Programing\python_exp\WebScraping\chromedriver', options=options)


def sendSmtpEmail(to, message):
    # creates SMTP session
    smtp = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    smtp.starttls()

    # Authentication
    smtp.login("scripnotifier@gmail.com", "kripsi291KRIPSI")

    # sending the mail
    smtp.sendmail('scripnotifier@gmail.com', to, message)


def ryzenInStock(model):
    message = """Subject: Stock Update!!!

                AMD RYZEN {} Processor Is In Stock!!!
                GO To: https://www.amd.com/en/direct-buy/sk
                """.format(model)
    return (message)


def radeonInStock(model):
    message = """Subject: Stock Update!!!

                AMD Radeon {} Graphics Is In Stock!!!
                GO To: https://www.amd.com/en/direct-buy/sk
                """.format(model)
    return (message)


def productParser():
    browser.get('https://www.amd.com/en/direct-buy/sk')
    products = browser.find_elements_by_xpath('//div[@class="direct-buy"]')

    for div in range(len(products)):
        if 'AMD Radeon™ RX 6800 XT Graphics' in products[div].text:
            RX_6800XT = products[div].text
        if 'AMD RYZEN™ 9 5900X Processor' in products[div].text:
            RYZEN_9_5900X = products[div].text
        if "AMD Radeon™ RX 6900 XT Graphics" in products[div].text:
            RX_6900XT = products[div].text

    # print(RX_6800_XT)
    # print(RYZEN_9_5900X)

    messages = []

    if "Out of Stock" not in RX_6800XT:
        messages.append(radeonInStock('RX 6800XT'))

    if "Out of Stock" not in RX_6900XT:
        messages.append(radeonInStock('RX 6900XT'))

    if "Out of Stock" not in RYZEN_9_5900X:
        messages.append(ryzenInStock('RYZEN 9 5900X'))

    # if "Out of Stock" not in RYZEN_7_5800X:
    #     return ryzenInStock('RYZEN 7 5800X')

    if messages == []:
        return None
    else:
        return messages


if __name__ == '__main__':
    messages = productParser()

    if messages:
        for message in messages:
            sendSmtpEmail('kripsoworld@gmail.com', message)
            toaster = ToastNotifier()
            toaster.show_toast("StockUpdate", message)

    browser.close()
    browser.quit()
