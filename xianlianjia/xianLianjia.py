# _*_ coding:utf-8 _*_

from myopener import makemyOpener
from bs4 import BeautifulSoup
from connectDB import inser_data

# 存储各区所有的房源信息
yan_ta = list()
chang_an = list()
lian_hu = list()
bei_lin = list()
ba_qiao = list()
wei_yang = list()

# 处理网页得到数据
def resolve_page(html):
    soup = BeautifulSoup(html, 'lxml')
    div_tags = soup.find_all('div', class_='info-panel')

    for div in div_tags:
        name = div.find('h2').find('a').string
        area = div.find('span', class_='region').string

        if (div.find('span', class_='num') != None):  # 可能存在楼盘房价待定
            print(div.find('span', class_='num'))
            price = div.find('span', class_='num').string

            if int(price) > 2000:   # 当小于2000时是按照万/套来算，直接舍去
                price = price + '元/平'
                item = area + ';' + name + ';' + price
                inser_data(name, area, price)   # 添加到数据库
                zone = item[0:2]
                switch = {     # 利用字典实现switch-case的功能
                    '雁塔': lambda x: yan_ta.append(x),
                    '长安': lambda x: chang_an.append(x),
                    '莲湖': lambda x: lian_hu.append(x),
                    '碑林': lambda x: bei_lin.append(x),
                    '灞桥': lambda x: ba_qiao.append(x),
                    '未央': lambda x: wei_yang.append(x)
                }
                try:
                    switch[zone](item)
                except KeyError as e:
                    pass

    return None

# 统计分析数据
def data_statistic():
    whole = dict()   # 各区平均房价
    strong = dict()   # 各区最高房价
    bottom = dict()   # 各区最低房价
    datas = list([yan_ta, chang_an, lian_hu, ba_qiao, bei_lin, wei_yang])
    for data in datas:
        total = 0
        heigh = 0
        h_str = ''
        low = 50000
        l_str = ''
        if len(data) > 0:
            area = data[0].split('-')[0]
            for info in data:
                price = int(info.split(';')[-1][:-3])
                if heigh < price:
                    heigh = price
                    h_str = info
                if low > price:
                    low = price
                    l_str = info
                total = total + price
            mean = total / len(data)
            whole[area] = mean
            strong[area] = h_str
            bottom[area] = l_str

    return whole, strong, bottom


# 主程序
def start():
    base_url = 'http://xa.fang.lianjia.com/loupan/pg'
    opener = makemyOpener()
    for i in range(1, 50):
        print('爬取第 %d 页：' % i)
        url = base_url + str(i) + '/'
        resp = opener.open(url, timeout=1000)
        page = resp.read().decode()
        resolve_page(page)

    all_mean, all_max, all_min = data_statistic()
    print('平均房价：\n', all_mean)
    print('--------------------------------------')
    print('最高房价：\n', all_max)
    print('--------------------------------------')
    print('最低房价：\n', all_min)

    return None

# 入口
if __name__ == '__main__':
    start()

