import pymysql

def get_data(sql):
    conn=pymysql.connect(host="localhost", user="root", password="653686", database="cmdb",charset="utf8")
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
def get_data1(sql):
    conn=pymysql.connect("localhost","root","1234","PY_Crawler",charset='utf8')
    cur = conn.cursor()
    cur.execute(sql)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
def search(sql,args):
    conn = pymysql.connect("localhost", "root", "1234", "PY_Crawler", charset='utf8')
    cur = conn.cursor()
    cur.execute(sql,args)
    conn.commit()
    cur.close()
    conn.close()
def check(sql,args):
    conn=pymysql.connect("localhost","root","1234","PY_Crawler",charset='utf8')
    cur = conn.cursor()
    cur.execute(sql,args)
    results = cur.fetchall()
    cur.close()
    conn.close()
    return results
def get_name(isbn):
    conn = pymysql.connect("localhost", "root", "1234", "PY_Crawler", charset='utf8')
    cur = conn.cursor()
    sql="select name from cmdb_bookinfo where ISBN='{}'".format(isbn)
    cur.execute(sql)
    results = cur.fetchall()

    text=[]
    for it in results:
        text.append(it[0])
    res=text[0]
    for i in range(1, len(text)):
        res=get_CommonSubstr(res,text[i])
    cur.close()
    conn.close()
    return res

def get_CommonSubstr(str1, str2):#求相同子串
    lstr1 = len(str1)
    lstr2 = len(str2)
    record = [[0 for i in range(lstr2 + 1)] for j in range(lstr1 + 1)]  # 多一位
    maxNum = 0  # 最长匹配长度
    p = 0  # 匹配的起始位

    for i in range(lstr1):
        for j in range(lstr2):
            if str1[i] == str2[j]:
                # 相同则累加
                record[i + 1][j + 1] = record[i][j] + 1
                if record[i + 1][j + 1] > maxNum:
                    # 获取最大匹配长度
                    maxNum = record[i + 1][j + 1]
                    # 记录最大匹配长度的终止位置
                    p = i + 1
    return str1[p - maxNum:p]