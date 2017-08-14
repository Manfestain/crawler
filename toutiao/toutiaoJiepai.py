# _*_ coding:utf-8 _*_

import requests
import json, re, os
from hashlib import md5
from urllib.parse import urlencode
from requests.exceptions import RequestException
from bs4 import BeautifulSoup

# 构造Ajax请求
def get_page_index(offset, keyword):
    parameter = {
        'offset': offset,
        'format': 'json',
        'keyword': keyword,
        'autoload': 'true',
        'count': '20',
        'cur_tab': '3'
    }
    url = 'http://www.toutiao.com/search_content/?' + urlencode(parameter)
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('构造Ajax请求出错')
        return None

# 解析索引页数据
def prase_page_index(html):
    data = json.loads(html)
    if data and 'data' in data.keys():
        for item in data.get('data'):
            yield item.get('article_url')

# 获取详情页数据
def get_page_detail(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('爬取详情页出错')
        return None

# 解析详情页数据
def prase_page_detail(html, url):
    soup = BeautifulSoup(html, 'lxml')
    title = soup.select('title')[0].get_text()
    pattern = re.compile(r'gallery:(.*?)]},', re.S)
    result = re.search(pattern, html)
    if result:
        temp = result.group(1).split(',"max_img_width"')[0] + '}'
        data = json.loads(temp)
        if data and 'sub_images' in data.keys():
            sub_images = data.get('sub_images')
            images = [item.get('url') for item in sub_images]
            for image in images:
                save_image_to_local(download_image(image))
            return {
                'title': title,
                'url': url,
                'images': images
            }

# 下载图片
def download_image(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            print('正在下载', url)
            return response.content   # 一般图片使用content，返回二进制流
        return None
    except RequestException:
        print('访问图片资源出错')
        return None

# 保存图片到本地
def save_image_to_local(content):
    file_path = '{0}/{1}/{2}.{3}'.format(os.getcwd(),'toutiaoImg', md5(content).hexdigest(), 'jpg')
    if not os.path.exists(file_path):
        with open(file_path, 'wb') as f:
            f.write(content)
            f.close()

# 主程序
def main(offset='0', keyword='街拍'):
    html = get_page_index(offset, keyword)
    for url in prase_page_index(html):
        html = get_page_detail(url)
        if html:
            prase_page_detail(html, url)

# 入口
if __name__ == '__main__':
    main()

    # 可以爬取多页数据
    # for i in range(0, 120, 20):
    #     main(i)

