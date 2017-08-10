# _*_ coding:utf-8 _*_

import sqlite3

db = sqlite3.connect('e:/workspace/pycharmcode/crawler/liajiadat.db')
db.isolation_level = None
db.execute('CREATE TABLE if not EXISTS Building(id integer primary key autoincrement, bname TEXt, area TEXT, price TEXT)')

# 插入数据
def inser_data(name, area, price):
    db.execute('INSERT INTO Building(bname, area, price) VALUES ("%s", "%s", "%s")' % (name, area, price))
    # db.execute('INSERT INTO Building( bname, area, price) VALUES ( "碑林", "蓝湖墅", "19000");')
    db.commit()

# 关闭数据库
def close_db():
    db.close()






