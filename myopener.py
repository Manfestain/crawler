# _*_ coding:utf-8 _*_
'使用build_opener自定义opener'

from urllib import request
from http import cookiejar

def makemyOpener(head = {
    'Connection': 'Keep-Alive',
    'Accept': 'text/html, application/xhtml+xml, */*',
    'Accept-Language': 'en-US,en;q=0.8,zh-Hans-CN,q=0.5,zh-Hans;q=0.3',
    'User-Agent': 'Mozilla/5.0(Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko'
}):
    cj = cookiejar.CookieJar()
    opener = request.build_opener(request.HTTPCookieProcessor(cj))
    header = []
    for key, value in head.items():
        elem = (key, value)
        header.append(elem)
    opener.addheaders = header
    return opener

# # 主调程序
# oper = makemyOpener()
# uop = oper.open('http://www.baidu.com/', timeout = 1000)
# data = uop.read()
# print(data.decode())