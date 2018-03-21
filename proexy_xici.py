#coding=utf-8


import requests
from lxml import etree
import json
import sqlite3
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()
import sys

headers = {
    "User-Agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36"
    }


def get_proxies():
    print u'西祠代理'
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
        html = requests.get(url, headers=headers).content
        tree = etree.HTML(html)
        parser = tree.xpath('//*[@id="ip_list"]/tr[position()>2]')
        for i in parser:
            ip = ['http://'+i.xpath('td[2]/text()')[0]+':'+i.xpath('td[3]/text()')[0]]
            ip = {'http':ip[0]}
            try:
                html = requests.get(conurl, headers=headers, proxies=ip, timeout=6).status_code
            except Exception,e:
                # print e
                html = 404
                print u'ip:%s不可用'%ip
            if html == 200: # 当ip可用时插入数据库
                license = 10
                sql = "INSERT INTO datas (`ip`, `license`) VALUES('%s','%s')"%(ip['http'],license) 
                try:
                    save_ip(sql) 
                except: # 当重复插入数据时忽略报错
                    print u'ip:%s已经存在数据库了'%ip
    urls = ['http://www.xicidaili.com/wt/'+str(i) for i in range(200)]
    pool = Pool(3)
    pool.map(parser,urls)
    pool.kill()
    pool.join()





if __name__ == '__main__':
    get_proxies()
