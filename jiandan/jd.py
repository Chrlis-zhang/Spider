#coding:utf-8

import time
import requests
import os
import time
import datetime
from bs4 import BeautifulSoup
# from pymongo import MongoClient

# client = MongoClient()
# db = client['jiandan']
# jiandan_collection = db['XXOO']

img_url = ''
data = ''

start_page = int(input('输入开始页面:'))
stop_page =  int(input('输入结束页面:'))

user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
headers = {'User-Agent': user_agent}

for ss in range(stop_page,start_page):
    print('开始请求页面,每3秒请求一次')
    time.sleep(3)
    res =requests.get('http://jandan.net/ooxx/page-%s#comments' %ss,headers=headers,)
    req = BeautifulSoup(res.text,'lxml').find_all('a',class_='view_img_link')
    print('请求页面为：http://jandan.net/ooxx/page-%s#comments' %ss)

    #去从 
    # for s in req:
    #     #print(s.get('href'))27
    #     img_url = 'http:%s' %s.get('href')
    #     if jiandan_collection.find_one({'img_url':img_url}):
    #         print('图片URL已存在')
    #     else:
    #         print('开始保存图片,当前图片URL为：',img_url)
    #         img_name = img_url[-17:-4]
    #         img_type = img_url[-3::]
    #         time.sleep(3)
    #         img = requests.get(img_url,headers=headers)
    #         post = {
    #             'img_url':img_url,
    #             'data':datetime.datetime.now()
    #         }
    #         jiandan_collection.save(post)
    #         f = open('D:\\11\%s' %(img_name) + '.%s' %img_type,'ab')
    #         f.write(img.content)
    #         f.close()

    for s in req:
        print(s.get('href'))
        img_url = 'http:%s' %s.get('href')
        img_type = img_url[-3::]
        img_name = img_url[-17:-4]
        time.sleep(3)
        img = requests.get(img_url,headers=headers)
        f = open('D:\\11\%s' %(img_name) + '.%s' %img_type,'ab')
        f.write(img.content)
        f.close()

