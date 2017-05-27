import requests
from bs4 import BeautifulSoup

res = requests.get('http://news.sina.com.cn/china')
res.encoding = 'utf-8'

soup = BeautifulSoup(res.text, 'html.parser')
news = soup.select('.news-item')##subShowContent1_news1 > div.first-news-item
for anews in news:
    if len(anews.select('h2')) > 0:
        h2 = anews.select('h2')[0].text
        a = anews.select('a')[0]['href']
        time = anews.select('.time')[0].text
        print(h2)
        print(a)
        print(time)