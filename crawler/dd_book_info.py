from bs4 import BeautifulSoup
import requests
import pymysql
import re
from lxml import etree
from mod import filter
import jsonpath
import urllib.request
import urllib.parse
import json

headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Connection": "close",
        }

def getddInfo(url):
    ID=url.strip("http://product.dangdang.com/").strip(".html")
    r = requests.get(url,headers=headers).text
    soup=BeautifulSoup(r,"html.parser")
    img_url='http:'+soup.find("img",id="largePic")["src"]
    try:
        saveImg(img_url,ID)
    except Exception as e:
        print("图片存储出错：",url,e)
    img = ID + ".jpg"

    name=filter(soup.find("h1")["title"])
    try:
        author=str(soup.find("span",dd_name="作者").find("a").string)
    except:
        author="无"
    
    publisher = str(soup.find("span", dd_name="出版社").find("a").string)
    price=float(soup.find("p",id="dd-price").text.strip().strip('¥'))
    isbn_out=soup.find("ul",class_="key clearfix")
    cnt=0
    for Li in isbn_out:
        if(cnt==5):
            isbn=Li.text
            break
        cnt=cnt+1
    isbn=isbn.strip("国际标准书号ISBN：")

    
    tree=etree.HTML(r)
    sale=tree.xpath('//*[@id="comm_num_down"]/text()')
    sales=int(sale[0])

    
    comments=c(url)

    db=pymysql.connect(host="localhost",port=3306,user='root',passwd="653686",db="cmdb",charset="utf8")
    cursor=db.cursor()

    sql = "select count(*) as cou from cmdb_bookinfo where website=%s limit 1"
    args = (url)
    cursor.execute(sql, args)
    results = cursor.fetchall()

    for item in results:
        if (item[0] == 0):
            # num,name,price,ISBN,author,pub,img,web,sales
            sql = "insert into cmdb_bookinfo(num,name,price,ISBN,author,publisher,img,website,sales,comment1,comment2,comment3,comment4,comment5,comment6,comment7,comment8,comment9,comment10) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
            args = [ID,name,price,isbn,author,publisher,img,url,sales,comments[0],comments[1],comments[2],comments[3],comments[4],comments[5],comments[6],comments[7],comments[8],comments[9]]
            #print(sql)
        else:
            pass
            """sql = "update cmdb_bookinfo set num=%s,name=%s, price=%s, isbn=%s, author=%s, publisher=%s, img=%s,sales=%s where website=%s"
            args = [ID,name,price,isbn,author,publisher,img,sales,url]"""
            #print(sql)
    try:
        cursor.execute(sql, args)
        db.commit()
        #print("成功写入数据库")
    except Exception as e:
        print("数据库错误1",e)
        db.rollback()

    cursor.close()
    db.close()

def saveImg(img_url,ID):
    img = requests.get(img_url, headers=headers).content
    img_name="D:\\导师制项目\\mysite\\cmdb\\static\\ddimage\\dd\\"+ID+".jpg"
    fout = open(img_name, 'wb')
    fout.write(img)
    fout.close()
def handle_request(url):
    request = urllib.request.Request(url=url, headers=headers)
    return request

def get_response(request):
    response = urllib.request.urlopen(request)
    return response

def parse_json(json_text):
    obj = json.loads(json_text)
    ret = jsonpath.jsonpath(obj, '$.data.list.html')
    return ret[0]
def c(url):
    ID=url.strip("http://product.dangdang.com/").strip(".html")
    r = requests.get(url,headers=headers).text
    categoryPath = re.findall(r'"categoryPath":"(.*?)"',r)
    categoryPath_str = "".join(categoryPath)
    url = "http://product.dangdang.com/index.php?r=comment%2Flist&productId=" + ID + "&categoryPath=" + categoryPath_str + "&mainProductId=" + ID + "&mediumId=0&pageIndex=1&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish&long_or_short=short"
    #print(url)
    json_text = get_response(handle_request(url=url)).read().decode('gbk')
    ret = parse_json(json_text)
    soup = BeautifulSoup(ret)
    commet_list = soup.select('.item_wrap > div')
    commet_list = str(commet_list)[1:-1]
    pattern = re.compile(r'''<div class="comment_items clearfix">
.*?
<em>(.*?)</em>
.*?
<span><a href="(.*?)" target="_blank">(.*?)</a></span>
.*?
<span>(.*?)</span>
.*?
<div class="support" data-comment-id="(.*?)">
.*?
<a class="pic" href="javascript:"><img alt="(.*?)" src="(.*?)"/></a>
.*?''', re.S)
    commet_list = pattern.findall(commet_list)
    if len(commet_list) <=10:
        nicklist=[]
        com_list=[]
        for commet in commet_list:
            nicklist.append(commet[5])
            com_list.append(commet[2])

        l=[]
        for i in range(len(commet_list)):
            l.append(nicklist[i]+':'+com_list[i])
        for i in l:
            if "追评" in i or "div" in i:
                l.remove(i)
        if len(l)<10:
            for i in range(len(l),10):
                l.append("*")
        #print(l)
        return l
    else:
        nicklist=[]
        com_list=[]
        for commet in commet_list:
            nicklist.append(commet[5])
            com_list.append(commet[2])

        l=[]
        for i in range(10):
            l.append(nicklist[i]+':'+com_list[i])
        for i in l:
            if "追评" in i or "div" in i:
                l.remove(i)
        #print(l)
        return l
