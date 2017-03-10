#coding:utf-8
import requests
import os
import datetime
import time
from bs4 import BeautifulSoup
from pymongo import MongoClient
#from proxy2 import request

class mzitu():

    def __init__(self):
        client = MongoClient()
        db = client['meinvxiezhenji']
        self.meizitu_collection = db['meizitu']
        self.title = ''
        self.url = ''
        self.img_url = []

    def all_url(self,url):
        html = self.request(url)   #不是用代理的时候使用
        #html = request.get(url,3)   #使用代理的时候使用
        all_a = BeautifulSoup(html.text,'lxml').find('div',class_='all').find_all('a')
        for a in all_a:
            title = a.get_text()
            if self.meizitu_collection.find_one({'标题': title}):
                print('标题已经存在，休息1秒后继续')
                time.sleep(1)
            else:
                self.title = title  # 新增
                print('开始保存', title)
                path = str(title).replace('?', '_')
                self.mkdir(path)
                os.chdir('I:\cc\\' + path)  # 新增
                href = a['href']
                # self.html(href)
                self.url = href  # 新增
                #if self.meizitu_collection.find_one({'主题页面': href}):  # 新增
                #    print('已爬页面,休息5秒后开始')
                #   time.sleep(5)
                #else:
                self.html(href)

    def html(self,href):
        html = self.request(href)   #不使用代理的时候使用
        #html = request.get(href,3)  #使用代理的时候使用
        max_span = BeautifulSoup(html.text,'lxml').find('div',class_='pagenavi').find_all('span')[-2].get_text()
        page_num = 0    #新增
        for page in range(1,int(max_span) + 1):
            page_num = page_num + 1
            page_url = href + '/' + str(page)
            self.img(page_url,max_span,page_num)    #新增 max_span、page_num

    def img(self,page_url,max_span,page_num):
        img_html = self.request(page_url)  #不使用代理的时候使用
        #img_html = request.get(page_url,3)  #使用代理的时候使用
        img_url = BeautifulSoup(img_html.text,'lxml').find('div',class_='main-image').find('img')['src']
        #self.save(img_url)
        self.img_url.append(img_url)    #新增
        if int(max_span) == page_num:   #新增
            self.save(img_url)
            post={
                '标题':self.title,
                '主题页面':self.url,
                '图片地址':self.img_url,
                '获取时间':datetime.datetime.now()
            }
            self.meizitu_collection.save(post)
            print('数据写入成功')
        else:
            self.save(img_url)


    def save(self,img_url):
        name = img_url[-9:-4]
        img = self.request(img_url)    #不使用代理的时候使用
        #img = request.get(img_url,3)    #使用代理的时候使用
        f = open(name + '.jpg' ,'ab')
        f.write(img.content)
        f.close()

    def mkdir(self,path):
        path = path.strip()
        isExists = os.path.exists(os.path.join('I:\cc\\',path))
        if not isExists:
            print('创建',path,'文件夹')
            os.mkdir(os.path.join('I:\cc\\',path))
            #os.chdir(os.path.join('I:\cc\\',path))
            return True
        else:
            print('文件夹',path,'已存在')
            return False
    #不使用代理的时候使用
    def request(self,url):
        headers = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
                   }
        content =requests.get(url,headers=headers)
        return content

Mzitu = mzitu()
Mzitu.all_url('http://www.mzitu.com/all')
