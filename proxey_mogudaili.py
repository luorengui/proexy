#coding=utf-8


import requests
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
    """
    获取Ip
    """
    pa = sys.path[0]
    print u'蘑菇代理'
    url = 'http://tianjin.12123.com/'
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
    def gevent(ip):
        """
        用协程检查ip是否可用，可用就存进数据库
        """
        global html
        conf_ip = {"http":ip}
        try:
            html = requests.get(url, headers=headers, proxies=conf_ip, timeout=10).status_code
        except Exception,e:
            print e
            html = 404
            print u'ip不可用%s'%ip
        if html == 200: # 当ip可用时插入数据库
            license = 10
            sql = "INSERT INTO datas (`ip`, `license`) VALUES('%s','%s')"%(ip,license) 
            try:
                save_ip(sql) 
            except Exception,e: # 当重复插入数据时忽略报错
                print u'ip:%s已经存在数据库了'%ip
    url = 'http://www.mogumiao.com/proxy/free/listFreeIp'
    html = requests.get(url).content
    datas = json.loads(html)
    data = datas['msg']

    ips = ['http:'+str(i['ip'])+':'+str(i['port']) for i in data]

    pool = Pool(3)
    pool.map(gevent,ips)
    pool.kill()
    pool.join()


if __name__ == '__main__':
    get_proxies()