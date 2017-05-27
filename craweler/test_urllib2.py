from urllib import request
import http.cookiejar

url = 'http://www.baidu.com'
test_url = 'http://baike.baidu.com/view/10812319.htm'
#第一种方法
print("第一种方法:")
response1 = request.urlopen(test_url)
#获取状态码
print(response1.getcode())
#读取内容
content1 = response1.read()
print(len(content1))

print("第二种方法:")
req = request.Request(url)
req.add_header("user-agent", "Mozilla/5.0")
response2 = request.urlopen(req)
#获取状态码
print(response2.getcode())
#读取内容
content2 = response2.read()
print(len(content2))

print("第三种方法:")
cj = http.cookiejar.CookieJar()
opener = request.build_opener(request.HTTPCookieProcessor(cj))
request.install_opener(opener)
response3 = request.urlopen(req)
#获取状态码
print(response3.getcode())
#读取内容
content3 = response3.read()
print(len(content3))
print(content3)
print(cj)
