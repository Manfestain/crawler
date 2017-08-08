# _*_ coding:utf-8 _*_

from urllib import request
from bs4 import BeautifulSoup
from myopener import makemyOpener
import uuid, os

url = 'http://www.socwall.com'
oper = makemyOpener()

# soup = BeautifulSoup(data.decode(), 'lxml')
# li_tag = soup.find_all('a', class_='image')

# 根据url请求页面
def request_page(url):
    rep = oper.open(url, timeout=1000)
    data = rep.read()
    return data.decode()

# 跳到下一页
def next_page(soup):
    next_href = soup.find('a', text='Next')
    print(next_href)
    return next_href.get('href')

# 解析页面标签
def resolve_page(data):
    soup = BeautifulSoup(data, 'lxml')
    return soup

# os.chdir(os.path.join(os.getcwd(), 'photos'))

def download_pic():
    i = 1
    next_url = url
    for page in range(0, 10):
        data = request_page(next_url)
        soup = resolve_page(data)

        li_tag = soup.find_all('a', class_='image')
        for tag in li_tag:
            img_src = tag.find('img').get('src')
            # print(url + img_src)
            src = url + img_src + '\n'
            with open('photos.txt', 'a') as f:
                f.write(src)
            print('第 %d 张图片完成' % i)
            i = i + 1

        next_url = url + next_page(soup)

if __name__ == '__main__':
    download_pic()
