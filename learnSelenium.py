# _*_ coding:utf-8 _*_

import unittest
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

'''
    driver = webdriver.Firefox()
    driver.get("http://www.python.org")
    assert 'Python' in driver.title
    elem = driver.find_element_by_name('q')
    elem.clear()
    elem.send_keys('pycon')
    elem.send_keys(Keys.RETURN)
    assert 'No results found'not in driver.page_source
    driver.close()
'''

# tests
class PythonOrgSearch(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Firefox()

    def test_search_in_python_org(self):
        driver = self.driver
        driver.get('http:www.python.org')
        self.assertIn('Python', driver.title)
        elem = driver.find_element_by_name('q')
        elem.send_keys('pycon')
        elem.send_keys(Keys.RETURN)
        assert 'no results found' not in driver.page_source

    def tearDown(self):
        # self.driver.close()
        pass

if __name__ == '__main__':
    unittest.main()

'''
    driver.back()   # 回退
    driver.forward()   # 前进
    
    # 定位元素
    elem = driver.find_element_by_id('tag id')
    elem = driver.find-element_by_name('tag name')
    elem = driver.find_element_by_class_name('tag class name')
    elem = driver.find_element_by_tag_name('tag name')
    elem = driver.find_element_by_link-text('link text')   # 当操作元素是一个文字链接时
    # 使用Xpath进行定位
    elem = driver.find_element_by_xpath('//input[@id='tag id']')   # 通过自身的id进行定位
    elem = driver.find_element_by_xpath('//span[@id='span id']/input')   # 通过上一级目录的id进行定位
    
    # 定位一组元素
    elems = find_elements_by_XXX('XXX')   # 使用find_elements来获取一组元素
    
    # 操作元素
    elem.clear()
    elem.send_keys('XXX')
    elem.click()   # 点击一个按钮
    elem.submit()   # 提交表单
    
    # webElement接口常用方法
    size = elem.size   # 返回元素的尺寸
    text = elem.text   # 返回元素的文本
    attr = elem.get_attribute('type')   # 返回元素的属性值
    
    driver.title   # 返回当前页面的title
    driver.cuttent_url  # 返回当前加载页面的url
    
    
'''

