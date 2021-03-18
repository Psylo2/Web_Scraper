import os
import requests
from bs4 import BeautifulSoup
"""
Create folder by given page number,
contain links that are related to given type,
extract content of each link un a link folder named

"""

cur = os.getcwd()
number_of_pages = int(input())
article_type = input()
url = f'https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page='
url_article = f'https://www.nature.com'
for cycle in range(1, number_of_pages + 1):
    try:
        os.mkdir(f"Page_{cycle}")
    except FileExistsError:
        pass
    os.chdir(f"{cur}\\Page_{cycle}")
    r = requests.get(f'{url}{cycle}')
    if r.status_code != 200:
        print('The URL returned', str(r.status_code) + '!')
    else:
        soup = BeautifulSoup(r.content, 'html.parser')
        for a in soup.find_all('div', {"class": "c-card__body"}):
            if a.find('span', {"class": "c-meta__type"}).text == article_type:
                link = a.a['href']
                b = a.text.splitlines()[2]
                b = b.replace(":", "")
                b = b.replace("?", "")
                b = b.replace("&", "")
                b = b.replace("+", "")
                b = b.replace("$", "")
                b = b.replace(",", "")
                b = b.replace("-", "")
                b = b.replace(" ", "_")
                with open('{}.txt'.format(b), 'wb') as file:
                    url2 = url_article + link
                    print(url2)
                    r2 = requests.get(url2, headers={'Accept-Language': 'en-US,en;q=0.5'})
                    soup2 = BeautifulSoup(r2.content, 'html.parser')
                    for t in soup2.find_all('div', {"class": "article-item__body"}):
                        content = ""
                        for x in t.find_all('p'):
                            content += (x.text + "\n")
                        print(content)
                        file.write(content.encode('utf-8'))

    os.chdir(cur)
print("Saved all articles.")
