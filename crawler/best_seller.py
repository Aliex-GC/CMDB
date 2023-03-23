import pymysql
import requests
from lxml import etree
import mod
from dd import ddmain
from dd_book_info import getddInfo

headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Connection": "close",
        }

def best_seller():
    url="http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-1"
    r = requests.get(url,headers=headers).text
    tree=etree.HTML(r)
    n=(tree.xpath("/html/body//div[@class='name']//@title"))
    urls=(tree.xpath("/html/body//div[@class='name']//@href"))
    names=[]
    for name in n:
        if name=="...":
            continue
        a=mod.filter(name)
        names.append(a)
    print(names)
    IDs=[]
    for url in urls:
        ID=url.strip("http://product.dangdang.com/").strip(".html")
        IDs.append(ID)
    #第二页
    
    url="http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-2"
    r = requests.get(url,headers=headers).text
    tree=etree.HTML(r)
    n1=(tree.xpath("/html/body//div[@class='name']//text()"))
    urls1=(tree.xpath("/html/body//div[@class='name']//@href"))
    for name in n1:
        n3=mod.filter(name)
        if name=="...":
            continue
        names.append(n3)
    for url in urls1:
        ID=url.strip("http://product.dangdang.com/").strip(".html")
        IDs.append(ID)
    url="http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent30-0-0-1-3"
    r = requests.get(url,headers=headers).text
    tree=etree.HTML(r)
    n2=(tree.xpath("/html/body//div[@class='name']//text()"))
    urls1=(tree.xpath("/html/body//div[@class='name']//@href"))
    for name in n2:
        n3=mod.filter(name)
        if name=="...":
            continue
        names.append(n3)
    for url in urls1:
        ID=url.strip("http://product.dangdang.com/").strip(".html")
        IDs.append(ID)
    print(len(names),len(IDs))

    db=pymysql.connect(host="localhost",port=3306,user='root',passwd="653686",db="cmdb",charset="utf8")
    cursor=db.cursor()

    sql = "truncate table cmdb_best_seller"
    cursor.execute(sql)

    sql = "insert into cmdb_best_seller(num,name) values(%s,%s)"
    print(sql) 
    for i in range(len(IDs)):
        args =[IDs[i],names[i]]
        try:
            cursor.execute(sql, args)
            db.commit()
        except Exception as e:
            print("数据库错误1",e)
            db.rollback()
    print("成功写入数据库!")
    cursor.close()
    db.close()    
best_seller()