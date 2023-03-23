import pymysql
import requests
from lxml import etree


headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Connection": "close",
        }

def hot_search():
    url="https://www.dangdang.com/"
    r = requests.get(url,headers=headers).text
    tree=etree.HTML(r)
    hot=tree.xpath("//*[@id='hd']/div[3]/div/div[3]//text()")
    hot=hot[2:8]
    print(hot)

    db=pymysql.connect(host="localhost",port=3306,user='root',passwd="653686",db="cmdb",charset="utf8")
    cursor=db.cursor()

    sql = "truncate table cmdb_hot_search"
    cursor.execute(sql)

    sql = "insert into cmdb_hot_search(name) values(%s)"
    print(sql) 
    for i in range(len(hot)):
        args =[hot[i]]
        try:
            cursor.execute(sql, args)
            db.commit()
        except Exception as e:
            print("数据库错误1",e)
            db.rollback()
    print("成功写入数据库!")
    cursor.close()
    db.close()
