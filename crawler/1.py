import requests
import os
headers ={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36",
            "Connection": "close",
        }
def saveImg(img_url,ID):
    img = requests.get(img_url, headers=headers).content
    img_name="mysite\cmdb\static\ddimage\dd\\"+ID+".jpg"
    fout = open(img_name, 'wb')
    fout.write(img)
    fout.close()
#saveImg("https://img3m9.ddimg.cn/32/30/29475599-1_w_25.jpg","29475599")
print(os.path.exists("D:\导师制项目\mysite\cmdb\static\ddimage\dd"))