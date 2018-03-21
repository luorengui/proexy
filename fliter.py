#coding=utf-8

import requests
import json
import sqlite3
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()
import sys


def filter_ip():
    pa = sys.path[0]
    url = 'http://tianjin.12123.com/'
    con = sqlite3.connect(pa+'\\ip.db')
    cursor = con.cursor()

    sql = "SELECT `ip` from datas"
    cursor.execute(sql)
    ips_tuple = cursor.fetchall()
    con.commit()
    con.close()
    def gevent(ip):
        con = sqlite3.connect(pa+'\\ip.db')
        cursor = con.cursor()
        
        ip = ip[0]
        print ip
        try:
            html = requests.get(url,proxies={'http':ip}, timeout=10).status_code
            print html
        except:
            html = 404
        if int(html) != 200:
            print u'ip%s不可用了'%ip
            sql = "DELETE from datas where ip='%s'"%ip
            cursor.execute(sql)
            con.commit()
            con.close()
    
    pool = Pool(5)
    pool.map(gevent,ips_tuple)
    pool.kill()
    pool.join()




if __name__ == '__main__':
    filter_ip()
