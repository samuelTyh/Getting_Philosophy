from urllib.parse import urljoin
import time
import re
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent


def get_1st_link(page):
    """This function is searching for the 1st link in wiki-page.

       Using fake_useragent to request the website's text,
       the all hyper-link we need are all include '/wiki/',
       find all then remove the link with parentheses:

       Args:
           page(type: str): Input url.

       Returns:
           page(type: str): The 1st link we got, if the input
           page is 'philosophy', then return origin page.

       """
    if page == 'https://en.wikipedia.org/wiki/Philosophy':
        return page

    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    req = requests.get(page, headers=headers)
    resp = req.text

    soup = BeautifulSoup(resp, 'lxml')
    content_div = soup.find('div', {'class': "mw-parser-output"})
    a_link_list = []
    for element in content_div.find_all('p', recursive=False):
        breaking = False
        for a_tag in element.find_all('a', recursive=False):
            a_link = a_tag.get('href')
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


def main():
    start = time.time()

    key = input('Start Page: ')
    page = 'https://en.wikipedia.org/wiki/' + key
    print(page)

    link = page
    past_link = []
    i = 0
    while i <= 30:
        if link != 'https://en.wikipedia.org/wiki/Philosophy':
            past_link.append(link)
            next_link = get_1st_link(link)
            if not next_link:
                print('No link in this page, try again!')
                break
            time.sleep(0.5)
            link = next_link
            i += 1
            if link in past_link:
                print("Oops! Link has repeated after %s times, keep it reality!." % i)
                break

            print('-' * 87)
            print(" %d : %s " % (i, link))
        else:
            print("Link %s times to get'Philosophy'" % i)
            break

    print('execute time: %s' % (time.time() - start))

if __name__ == "__main__":
    main()
