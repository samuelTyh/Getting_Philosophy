import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from fake_useragent import UserAgent
import time
import re


def get_1st_link(page):
    if page != 'https://en.wikipedia.org/wiki/Philosophy':
        ua = UserAgent()
        headers = {'User-Agent': ua.random}
        req = requests.get(page, headers=headers)
        resp = req.text
        # print(resp)
        # print('-'*87)

        soup = BeautifulSoup(resp, 'lxml')
        content_div = soup.find('div', {'class': "mw-parser-output"})
        a_link_list = []
        for element in content_div.find_all('p', recursive=False):
            breaking = False
            for a_tag in element.find_all('a', recursive=False):
                a_link = a_tag.get('href')
                # print(a_link)
                if bool(re.search("/wiki/.*", a_link)):
                    if not bool(re.search("/wiki/\w*\(+\w+\)+\w*", a_link)):
                        a_link_list.append(a_link)
                else:
                    breaking = True
                    break
            if breaking:
                break
        a_link = a_link_list[0]

        first_link = urljoin('https://en.wikipedia.org/', a_link)
        return first_link
    else:
        return page


def main():
    start = time.time()

    key = input('Start Page: ')
    page = 'https://en.wikipedia.org/wiki/' + key
    print(page)

    link = page
    past_link = []
    i = 0
    while i<=30:
        if link != 'https://en.wikipedia.org/wiki/Philosophy':
            past_link.append(link)
            next_link = get_1st_link(link)
            if not next_link:
                print('No link in this page, try again!')
                break
            time.sleep(0.5)
            link = next_link
            i+=1
            if link in past_link:
                print("Link has repeated, try another one.")
                break

            print('-' * 87)
            print(link)
        else:
            print("Link %s times to get'Philosophy'" % i)
            break

    print('execute time: %s' % (time.time() - start))

if __name__ == "__main__":
    main()



