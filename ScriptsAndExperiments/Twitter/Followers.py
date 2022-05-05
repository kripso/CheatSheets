from bs4 import BeautifulSoup
import requests
# handle = input('Input your account name on Twitter: ')
cookies = {"pwv": "2",
           "pws": "functional|analytics|content_recommendation|targeted_advertising|social_media"}
handle = 'kripsoworld'
page = requests.get('https://twitter.com/'+handle, cookies=cookies)
soup = BeautifulSoup(page.content, "html.parser")
try:
    print(soup.find_all())
except:
    print('Account name not found...')
