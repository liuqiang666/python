#coding:utf-8

from bs4 import BeautifulSoup
from urllib.parse import urljoin
import requests
import csv
import html5lib

URL = 'http://bj.ganji.com/fang1/p4/'
ADDR = 'http://bj.ganji.com/'

if __name__ == '__main__':
    start_page = 1
    end_page = 10
    price = 7
    with open('ganji.csv', 'wb') as f:
        csv_writer = csv.writer(f, delimiter=',')
        print('start......')
        while start_page <= end_page:
            start_page += 1
            print('get{0}'.format(URL.format(page=start_page, price=price)))
            response = requests.get(URL.format(page=start_page, price=price))
            html = BeautifulSoup(response.text, 'html.parser')#, from_encoding='utf-8'
            house_list = html.select('.f-list > .f-list-item > .f-list-item-wrap')
            if not house_list:
                break
            for house in house_list:
                house_title = str(house.select('.title > a')[0].string.encode('utf-8'))
                house_addr = str(house.select('.address > .area > a')[-1].string.encode('utf-8'))
                house_price = str(house.select('.info > .price > .num')[0].string.encode('utf-8'))
                house_url = urljoin(ADDR, house.select('.title > a')[0]['href'])
                house_data = [house_title, house_addr, house_price, house_url]
                csv_writer.writerow(house_data)
        print('end......')
