from bs4 import BeautifulSoup
import requests
import re
import jsonpath
import urllib.request
import urllib.parse
import json
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
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:72.0) Gecko/20100101 Firefox/72.0',

}
url="http://product.dangdang.com/23579654.html"
ID=url.strip("http://product.dangdang.com/").strip(".html")
r = requests.get(url,headers=headers).text
categoryPath = re.findall(r'"categoryPath":"(.*?)"',r)
categoryPath_str = "".join(categoryPath)
print(ID,categoryPath_str)
url1 = "http://product.dangdang.com/index.php?r=comment%2Flist&productId=" + ID + "&categoryPath=" + categoryPath_str + "&mainProductId=" + ID + "&mediumId=0&pageIndex=1&sortType=1&filterType=1&isSystem=1&tagId=0&tagFilterCount=0&template=publish&long_or_short=short"
print(url1)
json_text = get_response(handle_request(url=url1)).read().decode('gbk')
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
print(len(commet_list))
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
            l.append("")
    print(l)
        
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
            
    print(l)
        


