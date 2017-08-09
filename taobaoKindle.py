# _*_ coding:utf-8 _*_

import requests
import json
from collections import Counter

color = Counter()   # 记录kindle的颜色
typ = Counter()   # 记录kindle的套餐类型


# 每三十个字就换行
def add_enter(words):
    i = 0
    comment = ''
    for word in words:
        i = i + 1
        comment = comment + word
        if i % 30 == 0:
            comment = comment + '\n'
            i = 0
    return comment

# 保存评论到本地文件
def save_data(array, words):
    msg = ''
    for item in array:
        msg = msg + item + '\n'
    word = add_enter(words)
    msg = msg + word + '\n' + '==============' + '\n'

    with open('comments.txt', 'a') as f:
        f.write(msg)

    return None

# 解析json
def solve_json(json_data):

    for comment in json_data['rateList']:
        kind = comment['auctionSku']
        array = kind.split(';')
        typ.update(array[0][7])
        color.update(array[1][-2])
        words = comment['rateContent']
        save_data(array, words)

    return None


def start():
    base_url = 'https://rate.tmall.com/list_detail_rate.htm?itemId=522680881881&spuId=337259102&sellerId=2099020602&order=3&currentPage='

    for i in range(1, 11):
        url = base_url + str(i)
        req = requests.get(url)
        text = req.text[15:]   # 用text属性拿到字符串
        json_data = json.loads(text)
        solve_json(json_data)

    return None

# 主程序
if __name__ == '__main__':
    start()
    print('color :', color)
    print('Kind :', typ)


