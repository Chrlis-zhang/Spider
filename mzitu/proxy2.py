#coding:utf-8

import requests
import re
import random
import time
from lxml import etree


class download:
    def __init__(self):
        self.ip_list = []
        self.iplist = []
        user_agent = 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'
        headers = {'User-Agent': user_agent}
        timeout = 5     #代理超时时间
        html = requests.get('http://www.xicidaili.com/nn/',headers=headers).text    #获取代理的网站
        ip = etree.HTML(html).xpath('//table[contains(@id,"ip_list")]/tr/td[2]/text()') #提取代理IP
        prot = etree.HTML(html).xpath('//table[contains(@id,"ip_list")]/tr/td[3]/text()')   #提取代理端口
        for p in range(0,len(ip)):
            s = ""
            s += ip[p] + ':' + prot[p]
            self.ip_list.append(s.strip())  #拼接后的IP+端口放入ip_list
        for i in self.ip_list:
            prxy = {'http':'http://%s' %i}   #获取代理IP
            #try:
             #   d = requests.get('http://mzitu.com',  proxies=prxy, timeout=timeout)    #通过代理请求百度
             #   if d.status_code == 200:        #HTTP返回码如果是200，表明代理可用，加入代理列表
             #       print('代理', prxy, '可用，加入代理列表')
            self.iplist.append(prxy)
            #except:
             #   print('代理', prxy, '失败，')
        self.user_agent_list = [
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
    def get(self,url,timeout,proxy=None,num_retries=6):
        UA = random.choice(self.user_agent_list)
        headers = {'User-Agent':UA,
                   'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                   'Accept-Language': 'en-US,en;q=0.5',
                   'Connection': 'keep-alive',
                   'Accept-Encoding': 'gzip, deflate',
                   }
        if proxy == None:
            try:
                return requests.get(url,headers=headers,timeout=timeout)
                #response = requests.get(url,headers=headers,timeout=timeout)
                # if response.status_code == 200:
                #     return response
                #     #return requests.get(url,headers=headers,timout=timeout)
                # else:
                #     IP = ''.join(str(random.choice(self.iplist)).strip())
                #     proxy = {'http':IP}
                #     return self.get(url,timeout,proxy,)
            except:
                if num_retries > 0:
                    time.sleep(5)
                    print('获取网页出错，5S后获取倒数第',num_retries,'次')
                    return self.get(url,timeout,num_retries - 1)
                else:
                    print('开始使用代理')
                    time.sleep(5)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = IP
                    return self.get(url,timeout,proxy,)
        else:
            try:
                IP = ''.join(str(random.choice(self.iplist)).strip())
                proxy = IP
                # response = requests.get(url,headers=headers,proxies=proxy,timeout=timeout)
                # if response.status_code == 200:
                #     return response
                # else:
                #     if num_retries > 0:
                #         time.sleep(5)
                #         IP = ''.join(str(random.choice(self.iplist)).strip())
                #         proxy = {'http':IP}
                #         print(u'更换代理，5S后重新获取倒数第',num_retries,'次')
                #         print(u'当前代理IP是:',proxy)
                #         return self.get(url,timeout,proxy,num_retries - 1)
                #     else:
                #         print('代理失败，取消代理')
                #         return self.get(url,3)
                return requests.get(url,headers=headers,proxies=proxy,timeout=timeout)
            except:
                if num_retries > 0:
                    time.sleep(5)
                    IP = ''.join(str(random.choice(self.iplist)).strip())
                    proxy = IP
                    print('更换代理，5S后重新获取倒数第',num_retries,'次')
                    print('当前代理IP是：',proxy)
                    return self.get(url,timeout,proxy,num_retries - 1)
                else:
                    print('代理失败，取消代理')
                    return self.get(url,3)
request = download()
# CS = download()
# print(CS.get('http://mzitu.com',3),CS.iplist)



