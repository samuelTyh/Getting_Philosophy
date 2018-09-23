import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
import time

start = time.time()

key = input("What's the 1st: ")
page = 'https://en.wikipedia.org/wiki/'+ key
print(page)
print('-'*87)

ua = UserAgent()
headers = {'User-Agent': ua.random}
req = requests.get(page, headers=headers)
resp = req.text
# print(resp)
# print('-'*87)

soup = BeautifulSoup(resp, 'lxml')
content_div = soup.find('div', {'class': "mw-parser-output"})
for element in content_div.find_all('p', recursive=False)[:1]:
    print(element)
    print('-'*87)

#     if element.find('a', recursive=False):
#         article_link = element.find('a', recursive=False).get('href')
#         break
# first_link = urljoin('https://en.wikipedia.org/', article_link)
# print(first_link)
# print('-'*87)
#
# print('-'*87)
print('execute time: %s' % (time.time() - start))