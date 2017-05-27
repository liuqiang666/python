from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq
from multiprocessing import Pool
from 基础教程.craweler.taobao.config import *
import json 


browser = webdriver.PhantomJS(service_args=SERVICE_ARGS)
browser.set_window_size(1400, 900)
wait = WebDriverWait(browser, 10)
print('启动浏览器...')


def search():
    print('正在搜索...')
    try:
        browser.get("https://www.taobao.com/")
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#q"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#J_TSearchForm > div.search-button > button"))
        )
        input.send_keys(KEYWORD)
        submit.click()
        total = wait.until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.total"))
        )
        get_products()
        return total[0].text.strip()[1:-2]
    except TimeoutException:
        return search()


def next_page(pageNumber):
    print('正在翻页', pageNumber)
    try:
        input = wait.until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > input"))
        )
        submit = wait.until(
            EC.element_to_be_clickable((By.CSS_SELECTOR, "#mainsrp-pager > div > div > div > div.form > span.btn.J_Submit"))
        )
        input.clear()
        input.send_keys(pageNumber)
        submit.click()
        wait.until(
            EC.text_to_be_present_in_element((By.CSS_SELECTOR, '#mainsrp-pager > div > div > div > ul > li.item.active > span'), str(pageNumber))
        )
        get_products()
    except TimeoutException:
        return next_page(pageNumber)


def get_products():
    print('正在获取商品信息...')
    wait.until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "#mainsrp-itemlist .items .item"))
    )
    html = browser.page_source
    doc = pq(html)
    items = doc("#mainsrp-itemlist .items .item").items()
    for item in items:
        product = {
            'image': item.find('.pic .img').attr('src'),
            'price': item.find('.price').text(),
            'deal': item.find('.deal-cnt').text().strip()[:3],
            'title': item.find('.title').text(),
            'shop': item.find('.shop').text(),
            'location': item.find('.location').text()
        }
        print(product)
        write_to_file(product)


def write_to_file(content):
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(content, ensure_ascii=False) + '\n')
        f.close()


def main():
    try:
        total = search()
        total = int(total)
        # pool = Pool()
        # pool.map(next_page, [i for i in range(2, total + 1)])
        for i in range(2, total + 1):
            next_page(i)
    except Exception:
        print('出错啦')
    finally:
        browser.close()


if __name__ == '__main__':
    main()