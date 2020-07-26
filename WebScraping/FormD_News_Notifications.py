import requests
import json
from bs4 import BeautifulSoup
from win10toast import ToastNotifier


def get_news():
    request = requests.get("https://www.reddit.com/r/FormD/comments/hes1l5/latest_updates/", headers = {'User-agent': 'your bot 0.1'})
    soup = BeautifulSoup(request.content, 'html.parser')
    html = soup.select(".md")[2]

    text = html.text.strip()

    headers_html = html.select('h1')
    headers = []
    for header in headers_html:
        headers.append(header.text.strip())

    return headers, text

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
            send_email(new_data['message'][0])

def send_email(news):
    toast = ToastNotifier()
    toast.show_toast("FormD T1 News",news,duration=20,icon_path="icon.ico")
    pass

if __name__ == '__main__':

    news_headers, news_text = get_news()    
    get_latest_news(news_headers,news_text)
    

