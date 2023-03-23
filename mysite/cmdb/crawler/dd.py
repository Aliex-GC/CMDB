import requests
from lxml import etree
from cmdb.crawler import dd_book_info
from  multiprocessing.dummy import Pool
import time
def get_url(name):
    headers={
    "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36"
    }
    url="http://search.dangdang.com/?key={}&act=input".format(name)
    page_text=requests.get(url=url,headers=headers).text
    tree=etree.HTML(page_text)
    book_url = tree.xpath('//ul[@class="bigimg"]/li')
    url_list=[]
    for li in book_url: 
        try:
            urls=li.xpath('./a/@href')[0].strip()
            url_list.append("http:"+urls)
        except:
            pass

    return url_list  #若为搜到则返回空列表

def ddmain(bookname):
    #pool=Pool(5)
    print("爬虫开启中...")
    urls=get_url(bookname)
    #pool.map(dd_book_info.getddInfo,urls)
    for i in range(5):
        dd_book_info.getddInfo(urls[i])
        time.sleep(0.8)
    print("爬虫已完成！")

