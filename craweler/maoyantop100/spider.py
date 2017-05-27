from bs4 import BeautifulSoup
from requests import RequestException
from multiprocessing import Pool
import requests
import re
import json


def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None


def parse_one_page(html):
    soup = BeautifulSoup(html, 'lxml')
    indexs = soup.select('#app > div > div > div.main > dl > dd > i')
    images = soup.select('#app > div > div > div.main > dl > dd > a > img.board-img')
    titles = soup.select('#app > div > div > div.main > dl > dd > div > div > div.movie-item-info > p.name > a')
    actors = soup.select('#app > div > div > div.main > dl > dd > div > div > div.movie-item-info > p.star')
    times = soup.select('#app > div > div > div.main > dl > dd > div > div > div.movie-item-info > p.releasetime')
    score_integers = soup.select('#app > div > div > div.main > dl > dd > div > div > div.movie-item-number.score-num > p > i.integer')
    score_fractions = soup.select('#app > div > div > div.main > dl > dd > div > div > div.movie-item-number.score-num > p > i.fraction')
    datas = zip(indexs, images, titles, actors, times, score_integers, score_fractions)
    for index, image, title, actor, time, score_integer, score_fraction in datas:
        yield {
            'index': index.get_text(),
            'image': image['data-src'],
            'title': title['title'],
            'actor': actor.get_text().strip()[3:],
            'time': time.get_text().strip()[5:],
            'score': score_integer.get_text() + score_fraction.get_text()
        }


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main(offset):
    url = 'http://maoyan.com/board/4?offset=' + str(offset)
    html = get_one_page(url)
    for data in parse_one_page(html):
        print(data['index'], data['title'], data['score'])
        write_to_file(data)


if __name__ == '__main__':
    for i in range(10):
        main(i * 10)
    # offsets = [i * 10 for i in range(10)]
    # pool = Pool()
    # pool.map(main, offsets)#异步写入文件会导致文件写入不完整
    # for i in range(10):
    #     pool.apply_async(main, (i * 10,), callback=write_to_file)
    # pool.close()
    # pool.join()
