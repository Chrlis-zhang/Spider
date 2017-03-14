#coding:utf-8
'''
抓取tazhe.com漫画网站上面的漫画
用selenium来访问页面获取返回信息
程序写的比较粗糙，写入文件夹部分暂时也没做去重的判断

requests请求的时候，需要res.encoding = 'utf-8'
'''
import requests
import os
from selenium import webdriver
from bs4 import BeautifulSoup

phantomjsdriver = 'C:\Program Files (x86)\phantomjs\\bin\phantomjs.exe'

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'

headers = {'User-Agent': user_agent}

browser = webdriver.PhantomJS(phantomjsdriver)

browser.get('http://www.tazhe.com/mh/14027/')   #要抓取的漫画页面

text = browser.page_source  #返回页面的源码

mn_list = BeautifulSoup(text,'lxml').find('div',class_='plist pnormal').find_all('a')   #获取当前漫画列表，一共多少话

for mn_url in mn_list:
    browser.get('http://www.tazhe.com%s' % (mn_url.get('href')))  # 访问漫画列表，按照默认排序访问
    text2 = browser.page_source
    #print(text2)
    mn_names = BeautifulSoup(text2, 'lxml').find('title').get_text()    #漫画详情页面的title,创建文件夹使用
    img_title = BeautifulSoup(text2, 'lxml').find('h1').get_text()      #
    imgs = BeautifulSoup(text2, 'lxml').find('div', class_='tbCenter').find('img', class_='52tianmanhua')
    pages = BeautifulSoup(text2, 'lxml').find('div', class_='picNav').find_all('option')[-1].get('value')
    for s in range(1,int(pages) + 1):   #抓取页面包含的图片并保存
        browser.get('http://www.tazhe.com%s?p=%s' %(mn_url.get('href'),s)) #访问漫画页面
        text3 = browser.page_source
        imgs_url = BeautifulSoup(text3,'lxml').find('div',class_='tbCenter').find('img').get('src') #找到当前页面的图片URL
        imgs_name = str(s) + '_' + imgs_url[-10:-4]     #下载图片的名称，str(s) 主要是排序
        imgs_download = requests.get(imgs_url,headers=headers)  #访问图片URL
        isExists = os.path.exists(os.path.join('I:\\ff\\', mn_names.strip()))
        if not isExists:
            os.mkdir(os.path.join('I:\\ff\\', mn_names.strip()))
            os.chdir('I:\\ff\\' + mn_names.strip())
        else:
            os.chdir('I:\\ff\\' + mn_names.strip())
        f =open(imgs_name + '.jpg', 'ab')
        f.write(imgs_download.content)
        f.close()
