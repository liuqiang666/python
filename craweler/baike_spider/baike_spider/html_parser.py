from bs4 import BeautifulSoup
import re
import urllib.parse


class HtmlParser(object):


    def _get_new_urls(self, page_url, soup):
        new_urls = set()
        # /view/123.htm
        #http://paper.people.com.cn/rmrb/html/2017-03/19/nw.D110000renmrb_20170319_1-01.htm
        #http://paper.people.com.cn/rmrb/html/2017-03/19/nbs.D110000renmrb_01.htm
        links = soup.find_all('a', href=re.compile(r"nw.D110000renmrb_\d+_\d-\d{2}.htm|nbs.D110000renmrb_\d{2}.htm"))#r"/vie w/\d+\.htm"
        for link in links:
            new_url = link['href']
            new_full_url = urllib.parse.urljoin(page_url, new_url)
            new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):

        res_data = {}

        #url
        res_data['url'] = page_url
        message = re.search(r"_(\d{4})(\d{2})(\d{2})_\d-(\d{2})\.", res_data['url'])
        year = message.group(1)
        month = message.group(2)
        day = message.group(3)
        res_data['time'] = year + "-" + month + "-"+ day
        res_data['page'] = str(int(message.group(4)))#在page = '01'时，把前面的0去掉
        print("时间:%s" % res_data['time'])
        print("版面:%s" % res_data['page'])
        #<dd class="lemmaWgt-lemmaTitle-title"> <h1>Python</h1>
        #title_node = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1')

        #<div class="text_c"><br><h1>习近平会见美国国务卿蒂勒森</h1>
        try:
            title_node = soup.find("h1")#find('div', class_="text_c").
            res_data['title'] = title_node.get_text()
            print("标题:%s" % res_data['title'])
        except:
            print("title error")

        #<div class="lemma-summary" label-module="lemmaSummary">

        #<div class="lai" style="padding-top: 5px;">
        #   res_data['message'] = time_node.get_text()
         #   print("信息:%s" % res_data['message'])
            #（2017年03月20日 21版）
         #   message = re.search(r"(\d{4}年\d{2}月\d{2}日).*(\d{2}).*版", res_data['message'])
         #   res_data['time'] = message.group(1)
         #   res_data['page'] = message.group(2)


        #except:
         #   print("time error")

        #<div id="ozoom" style="-ms-zoom: 100%;">
        try:
            content_nodes = soup.select('#ozoom > p')#soup.find('p').find('div', class_="c_c").find('div').
            res_data['content'] = ""
            for content_node in content_nodes:
                content = content_node.get_text()
                res_data['content'] = res_data['content'] + content

            print("content length:%d" % len(res_data['content']))
            #for content_node in content_nodes:
             #   res_data['content'] = res_data['content'] + content_node.get_text()
        except:
            print("content error")
        return res_data


    def parse(self, page_url, html_cont):
        if page_url is None or html_cont is None:
            return
        print("parse:")
        soup = BeautifulSoup(html_cont, 'html.parser', from_encoding='utf-8')
        new_urls = self._get_new_urls(page_url, soup)
        print("获取数据：")
        if (re.search(r"nw.D110000renmrb_\d+_\d-\d{2}.htm", page_url)):
            new_data = self._get_new_data(page_url, soup)
        else:
            new_data = None
        return new_urls, new_data
