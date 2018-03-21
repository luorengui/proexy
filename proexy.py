#coding=utf-8


import sqlite3
import random
# import requests

# 随机获取一个ip地址
def Proxies(retire_num=3):
    url = 'http://tianjin.12123.com/'
    con = sqlite3.connect('ip.db')
    cursor = con.cursor()
    sql = "SELECT `ip` from datas"
    cursor.execute(sql)
    ips_tuple = cursor.fetchall()
    con.commit()
    con.close()
    ip = {'http':random.choice(ips_tuple)[0]}
    # html = requests.get(url,proxies=ip).status_code
    # if html !=
    return ip



if __name__ == '__main__':
    print Proxies()
