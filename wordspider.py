import json
import time

import MySQLdb
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import InvalidArgumentException

#options = webdriver.ChromeOptions()
#options.add_argument('headless')
#chrome = webdriver.Chrome(chrome_options=options)

chrome = webdriver.Chrome()
chrome.get('https://www.shanbay.com')

cookie = open('C:\\Users\\kenny\\cook.json','r')
for i in json.load(cookie):
    try:
        chrome.add_cookie(i)
    except InvalidArgumentException:
        del i['expiry']
        chrome.add_cookie(i)
chrome.refresh()

chrome.find_element_by_link_text('单词').click()
time.sleep(3)
chrome.find_element_by_class_name('index_vocabularyLink__1c7FY').click()
time.sleep(3)
chrome.find_element_by_xpath("//div[@class='index_navItem__1Fbwq'][@id='3']").click()
time.sleep(3)

pages = chrome.find_elements_by_xpath("//ul[@class='index_pageContainer__2l7E1']/li")[-2].text

def download(page):
    app = MySQLdb.connect(user='root',passwd='xuchan1128',db='app',charset='utf8')
    cursor = app.cursor()

    for p in range(page):
        words = {}
        en = chrome.find_elements(By.CLASS_NAME, 'index_wordName__1lkbV')
        ch = chrome.find_elements_by_xpath("//div[@class='index_bottom__XLoPQ']/span[not(@class)]")
        category = chrome.find_elements_by_xpath("//span[@class='index_pos__38JdC']")
        for i in range(len(en)):
            if len(en) > 10:
                print(len(en))
                quit()
            enkeys = en[i].text
            chkeys = ch[i].text
            catkeys = category[i].text
            words[i] = [enkeys,chkeys,catkeys]
            sql = "INSERT INTO backend_cte6(en,ch,category) values(%s,%s,%s)"
            cursor.execute(sql,(words[i][0],words[i][1],words[i][2]))
            app.commit()
        print('已获取到{}页'.format(p))
        time.sleep(3)
        chrome.find_elements_by_xpath("//ul[@class='index_pageContainer__2l7E1']/li")[-1].click()
        time.sleep(5)
    cursor.close()
    app.close()  

try:
    userpage = int(input('共有{}页单词,你需要获取多少页\n'.format(pages)))
    download(userpage)
except ValueError:
    print('请输入正确的数字')
    userpage = input()
    download(userpage)
finally:
    if type(userpage) is str:
        print('fuck you!')
        quit()

