from bs4 import BeautifulSoup
import re

html_doc = """
<html><head><title>The Dormouse's story</title></head>
<body>
<p class="title"><b>The Dormouse's story</b></p>

<p class="story">Once upon a time there were three little sisters; and their names were
<a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
<a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
<a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
and they lived at the bottom of a well.</p>

<p class="story">...</p>
"""

soup = BeautifulSoup(html_doc, "html.parser", from_encoding="utf-8")
print("获取所有的连接")
links = soup.find_all('a')
for link in links:
    print(link.name, link['href'], link.get_text())

print("获取lacie的链接")
link_node = soup.find("a", href="http://example.com/lacie")
print(link_node.name, link_node['href'], link_node.get_text())

print("段落文字匹配")
p_node = soup.find("p", class_="story")
print(p_node.name, p_node.get_text())




text = '''《
          人民日报
          》（
          2017年03月20日

          01
          版）
'''
test_url = "http://paper.people.com.cn/rmrb/html/2017-03/19/nw.D110000renmrb_20170319_1-01.htm"
print(type(text))
#(\d{4}[\u4E00-\u9FA5]\d{2}[\u4E00-\u9FA5]\d{2}[\u4E00-\u9FA5]).+(\d{2}).+[\u4E00-\u9FA5]
message = re.search(r"_(\d{8})_\d-(0?\d|\d{2})\.",test_url)
print(message.group())
print(message.group(1))
m = message.group(2)
mi = int(m)
print(type(mi))
ms = str(mi)
print(ms)