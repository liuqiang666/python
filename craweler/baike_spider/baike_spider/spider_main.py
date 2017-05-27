import time

from 基础教程.craweler.baike_spider.baike_spider import html_downloader
from 基础教程.craweler.baike_spider.baike_spider import html_outputer
from 基础教程.craweler.baike_spider.baike_spider import html_parser
from 基础教程.craweler.baike_spider.baike_spider import output_mysql
from 基础教程.craweler.baike_spider.baike_spider import url_manager


class SpiderMain(object):
    def __init__(self):
        self.urls = url_manager.UrlManager()
        self.downloader = html_downloader.HtmlDownloader()
        self.parser = html_parser.HtmlParser()
        #self.outputer = html_outputer.HtmlOutputer()
        self.outputer = output_mysql.OutputMysql()

    def craw(self, root_url):
        self.urls.add_new_url(root_url)
        count = 1

        while self.urls.has_new_url():
            try:
                new_url = self.urls.get_new_url()

                #if new_url == 'http://baike.baidu.com/view/10812319.htm':
                   # continue

                print('craw %d:%s' %(count, new_url))
                html_cont = self.downloader.download(new_url)
                new_urls, new_data = self.parser.parse(new_url, html_cont)
                print("添加url")
                self.urls.add_new_urls(new_urls)
                self.outputer.collect_data(new_data)

                if count == 1000:
                    break

                count += 1
            except:
                print("craw failed")

        #self.outputer.outout_html()
        self.outputer.output_mysql()


if __name__=="__main__":
    now_time = time.strftime('%Y-%m/%d',time.localtime(time.time()))
    #root_url = "http://paper.people.com.cn/rmrb/html/" + now_time + "/nbs.D110000renmrb_01.htm"
    root_url = "http://paper.people.com.cn/rmrb/html/2017-03/24/nbs.D110000renmrb_01.htm"
    obj_spider = SpiderMain()
    obj_spider.craw(root_url)