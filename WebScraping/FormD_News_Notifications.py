import json
import requests 
from bs4 import BeautifulSoup
from contextlib import closing
from win10toast import ToastNotifier
from requests.exceptions import RequestException


def simple_get(url):
    try:
        with closing(requests.get(url, stream=True, headers = {'User-agent': 'your bot 0.1'})) as response:
            if is_good_response(response):
                return response.content
            else:
                return None

    except RequestException as exception:
        log_error('Error during requests to {0} : {1}'.format(url, str(exception)))
        return None


def is_good_response(response):
    content_type = response.headers['Content-Type'].lower()
    return (response.status_code == 200 and content_type is not None and content_type.find('html') > -1)

def log_error(exception):
    send_notification(exception)

def get_news(url):
    content = simple_get(url)

    if content is not None:
        soup = BeautifulSoup(content, 'html.parser')
        html = soup.select(".md")[2]

        text = html.text.strip()

        headers_html = html.select('h1')
        headers = []
        for header in headers_html:
            headers.append(header.text.strip())

        return headers, text

    raise log_error('Error retrieving contents at {}'.format(url))

def get_latest_news(headers, text):
    newBlock = text.split(headers[1])
    
    with open("C:/Users/kripso/Documents/Programing/python_exp/WebScraping/formD_new.json") as json_file:
        new_data = {}
        new_data['message'] = []
        new_data['message'].append(newBlock[0])

        data = json.load(json_file)

        if data['message'] != new_data['message']:
            with open('C:/Users/kripso/Documents/Programing/python_exp/WebScraping/formD_new.json', 'w') as json_file:
                json.dump(new_data, json_file)
            send_notification(new_data['message'][0])

def send_notification(news):
    toast = ToastNotifier()
    toast.show_toast("FormD T1 News",news,duration=20,icon_path="icon.ico")
    pass

if __name__ == '__main__':
    url = "https://www.reddit.com/r/FormD/comments/hes1l5/latest_updates/"
    news_headers, news_text = get_news(url)    
    get_latest_news(news_headers,news_text)
    

