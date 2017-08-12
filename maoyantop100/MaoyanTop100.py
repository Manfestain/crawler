# _*_ coding:utf-8 _*_

import re, json
import requests
from multiprocessing import Pool
from requests.exceptions import RequestException

# 爬取单页源码
def get_one_page(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        return None

# 解析网页的数据
def prase_one_page(html):
    pattern = re.compile(r'<dd>.*?board-index.*?>(\d+)</i>'
                         + '.*?data-src="(.*?)".*?'
                         + 'name"><a.*?>(.*?)</a>'
                         + '.*?star">(.*?)</p>'
                         + '.*?releasetime">(.*?)</p>'
                         + '.*?integer">(.*?)</i>.*?fraction">(.*?)</i>'
                         + '.*?</dd>', re.S)  # re.S匹配任意字符，包括回车
    items = re.findall(pattern, html)

    for item in items:
        yield{
            'index': item[0],
            'name': item[2],
            'actor': item[3].strip()[3:],
            'time': item[4].strip()[5:],
            'score': item[5] + item[6],
            'image': item[1],
        }

# 保存到本地
def save_to_local(data):
    with open('top100.txt', 'a', encoding='utf-8') as f:
        f.write(json.dumps(data, ensure_ascii=False) + '\n')
        f.close()

# 主程序
def main(i):
    url = 'https://maoyan.com/board/4?offset=' + str(i)
    html = get_one_page(url)

    for item in prase_one_page(html):   # prase_one_page使用了生成器
        save_to_local(item)


# 入口
if __name__ == '__main__':
    for i in range(0, 100, 10):
        main(i)

# 使用多进程抓取
# if __name__ == '__main__':
#     pool = Pool()
#     pool.map(main, [i for i in range(0, 100, 10)])