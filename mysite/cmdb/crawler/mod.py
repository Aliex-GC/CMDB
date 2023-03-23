import re
def filter(str):
    res=re.sub(r'（.*',"",str)
    res = re.sub(r'\(.*', "", res)
    return res
