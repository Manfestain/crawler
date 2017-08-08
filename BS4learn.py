# _*_ coding:utf-8 _*_

from bs4 import BeautifulSoup, CData, NavigableString
import re

html_doc = """
        <html><head><title>The Dormouse's story</title></head>
        <body>
        <title>this is another title</title>
        <p class="title"><b>The Dormouse's story</b></p>
        
        <p class="story">Once upon a time there were three little sisters; and their names were
        <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
        <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
        <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
        and they lived at the bottom of a well.</p>
        
        <p class="story">...</p>
"""

soup1 = BeautifulSoup(html_doc, 'lxml')
# print(soup1.prettify())   # 解析该段代码，得到标准的输出

print(soup1.title)   # 当有多个title时，默认取第一个
print(soup1.title.string)
print(soup1.title.parent.name)
print(soup1.p)
print(soup1.p['class'])
print(soup1.a)

for link in soup1.find_all('a'):   # 可以使用循环找到所有的<a>标签
    print(link.get('href'))
print(soup1.find_all('a'))   # 返回一个list，包含了所有的<a>标签

print(soup1.get_text())   # 获取所有的文字

print('--------------------------BS中的四种对象------------------------')
# 第一种对象：tag
tag = soup1.p
print(tag)
print(type(tag))
print(tag.name)
print(tag.string)
print(tag['class'])
print(tag.attrs)

tag['id'] = 1   # 可任意添加属性
print(tag)
print(tag.attrs)   # 当有多个属性时，返回一个字典

soup2 = BeautifulSoup('<p class="body strikeout"></P>', 'lxml')
print(soup2.p['class'])  # 多值属性会返回一个list，当该标签没有被定义为多值属性时，返回一个字符串
soup2.p['id'] = 'my id'
print(soup2.p['id'])
print(type(soup2.p['id']))

# 第二种对象：NavigableString
print(type(tag.string))  # 使用NavigableString来包装tag中的字符串
tag.string.replace_with('no longer bold')
print(tag)
tag.name = 'r'
print(tag)

# 第三种对象：BeautifulSoup
print(soup2.name)

# 第四种对象：comment,主要针对文档中注释部分,是一种特殊的NavigableString
markup = "<b><!--hey, want to buy a used parser?--></b>"
soup3 = BeautifulSoup(markup, 'lxml')
comment = soup3.b.string
print(comment)
print(soup3.b.prettify())
cdate = CData('A cdate block')
comment.replace_with(cdate)
print(soup3.b.prettify())

print('-----------------------------遍历文档树-----------------------------------')
soup4 = BeautifulSoup(html_doc, 'lxml')
print(soup4.body.p.b)
head_tag = soup4.head
print(head_tag.contents)   # 将tag的子节点以列表的方式输出
title_tag = head_tag.contents[0]
print(title_tag)
print(title_tag.contents)

print(len(soup4.contents))
print(soup4.contents[0].name)

for child in head_tag.children:  # 利用.children可以对tag的子节点进行循环
    print(child)
for string in soup4.strings:
    print('1 :', repr(string))
for string in soup4.stripped_strings:  # 可以使用该方法过滤掉空格或空行
    print('2 :', repr(string))

html_tag = soup4.html
print(type(html_tag.parent))
print(soup4.parent)

link = soup4.a
for parent in link.parents:
    # if parent is None:
    #     print(parent)
    # else:
        print(parent.name)

# 兄弟节点
sibling_soup = BeautifulSoup('<a><b>text1</b><c>text2</c></b></a>', 'lxml')
print(sibling_soup.prettify())
print(sibling_soup.b.next_sibling)
for sibling in soup4.a.next_siblings:
    print('1 :', repr(sibling))
for sibling in soup4.find(id='link3').previous_siblings:
    print('2 :', repr(sibling))

# 回退和前进
last_a_tag = soup4.find('a', id='link3')
print(last_a_tag.next_sibling)
print(last_a_tag.next_element)
print(last_a_tag.next_element.next_element)

print('----------------------------------过滤器--------------------------------')
for tag in soup4.find_all(re.compile(r'^b')):  # 可以传入正则表达式，则使用match()方法取匹配
    print(tag)
print(soup4.find_all(['a', 'b']))

def has_class_but_no_id(tag):   # 自定义过滤器方法，方法接收一个参数
    return tag.has_attr('class') and not tag.has_attr('id')
print('*********filter*********')
print(soup4.find_all(has_class_but_no_id))
print(len(soup4.find_all(has_class_but_no_id)))

def surrounded_by_strings(tag):
    return (isinstance(tag.next_element, NavigableString)
            and isinstance(tag.previous_element, NavigableString))
for tag in soup4.find_all(surrounded_by_strings):
    print(tag.name)

soup5 = BeautifulSoup('<div data-foo="value">foo!</div><div data="value">foo!</div>', 'lxml')
print(soup5.find_all(attrs={'data-foo': 'value'}))
print(soup4.find_all('a', class_='sister'))   # 直接用class的话会起冲突

print('-------------------------------CSS选择器----------------------------')
print(soup4.select('title'))
print(soup4.select('body a'))  # 逐层查找
print(soup4.select('html head title'))
print(soup4.select('head > title'))  # 找到head下的直接title标签
print(soup4.select('p > a'))
print(soup4.select('#link1'))  # 通过tag的id进行查找
print(soup4.select('.sister'))   # 通过css的类名查找
print(soup4.original_encoding)
soup4.from_encoding = 'iso-8859-8'
print(soup4.original_encoding)