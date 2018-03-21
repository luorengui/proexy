#coding=utf-8


import requests
import lxml.html
import json
import sqlite3
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()
import sys
import time

headers = {
    "Host":"www.kuaidaili.com",
    "Referer":"https://www.kuaidaili.com/free/inha/2/",
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }

def get_proxies():
    print u'快代理'
    pa = sys.path[0]
    conurl = 'http://tianjin.12123.com/'
    def save_ip(sql):
        """
        将ip存进数据库
        """
        con = sqlite3.connect(pa+'\\ip.db')
        con.execute(
            """CREATE TABLE IF NOT EXISTS datas(
            -- id integer primary key NOT NULL,
            ip varchar primary key NOT NULL,
            license int NOT NULL
            );""")
        con.execute(sql)
        con.commit()
        con.close()

    def parser(url):
        print url
        html = requests.get(url, headers).content
        # print html
        tree = lxml.html.fromstring(html)
        data = tree.cssselect('#list > table > tbody > tr')
        for td in data:
            for i in td.cssselect('td:nth-child(1)'):
                ip = i.text_content()
            for i in td.cssselect('td:nth-child(2)'):
                port = i.text_content()
            ip = {'http':'http'+'://'+ip+':'+port}
            try:
                html = requests.get(conurl, headers=headers, proxies=ip, timeout=5).status_code
            except Exception,e:
                # print e
                html = 404
                print u'ip:%s不可用'%ip
            if html == 200: # 当ip可用时插入数据库
                license = 10
                print u'ip:%s可用'%ip
                sql = "INSERT INTO datas (`ip`, `license`) VALUES('%s','%s')"%(ip['http'],license) 
                try:
                    save_ip(sql) 
                except: # 当重复插入数据时忽略报错
                    print u'ip:%s已经存在数据库了'%ip
    urls = ['https://www.kuaidaili.com/free/inha/%s/'%i for i in range(1,20)]
    print urls
    pool = Pool(1)
    pool.map(parser,urls)
    pool.kill()
    pool.join()



if __name__ == '__main__':
    get_proxies()