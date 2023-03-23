# -*-coding:utf-8 -*-
from django.shortcuts import render,HttpResponseRedirect,HttpResponse
from cmdb.models import UserModel
from cmdb.models import BookInfo
from cmdb.models import MyCollect
from cmdb.models import Best_seller
from cmdb.models import hot_search
from django.db import models
from cmdb.crawler.dd import ddmain
from cmdb.web_func import get_data

# Create your views here.
def index(request):
    name = request.session.get('name')
    if request.method == "GET":
        books =hot_search.objects.all()
        #return HttpResponse(books)
        return render(request, 'main.html',{'name':name,"books":books})
    if request.method == "POST":
        bookname = request.POST.get('bookname')
        #return HttpResponse(bookname)
        return HttpResponseRedirect('/query/?name='+bookname)
    else:
            ddmain(bookname)
            books = BookInfo.objects.filter(name__contains=bookname).all()
            i=1
            for book in books:
                book.i1=i
                i+=1
            return render(request, 'query_result.html',{'books':books})
        
 
def login(request):
    if request.method == "GET":
        return render(request, 'login.html')
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        # 验证用户名和密码，验证通过的话，返回user对象
        
        userModel = UserModel.objects.filter(username=username, password=password).first() 
        
        if userModel:
            request.session['name']=username
            return HttpResponseRedirect('/index/')
        else:
            hint="账户名或密码错误"
            return render(request, 'login.html',{'hint':hint})
def register(request):
    if request.method == 'GET':
        return render(request, 'register.html')
    if request.method == 'POST':
        username = request.POST.get("username",None)
        password = request.POST.get("password",None)
        userModel = UserModel.objects.filter(username=username).first()
        if userModel:
            hint="账号密码已存在！"
            return render(request, 'register.html',{"hint":hint})
        UserModel.objects.create(username=username, password=password)
        return HttpResponseRedirect('/login/')
def query(request):
    if request.method == 'GET':
            bookname=request.GET.get("name")
            name = request.session.get('name')
            request.session['bookname']=bookname
            books = BookInfo.objects.filter(name__contains=bookname).all()
            if books:
                i=1
                for book in books:
                    book.i1=i
                    i+=1
                    this=MyCollect.objects.filter(username=name,num=book.num)
                    if this:
                        book.hint="已收藏"
                    else:
                        book.hint="加入收藏"
            else:
                ddmain(bookname)
                books = BookInfo.objects.filter(name__contains=bookname).all()
                i=1
                for book in books:
                    book.i1=i
                    i+=1
                this=MyCollect.objects.filter(username=name,num=book.num)
                if this:
                    book.hint="已收藏"
                else:
                    book.hint="加入收藏"
            return render(request, 'query_result.html',{'books':books})


def qurey_book_details(request):
    if request.method == 'GET':
            id=request.GET.get("id")
            book=BookInfo.objects.filter(num=id).first()
            return render(request, 'book_details.html',{'book':book})
        
def query_collect(request):
    if request.method == 'GET':
        name = request.session.get('name')
        bookname=request.session.get('bookname')
        num=request.GET.get("num")
        book=BookInfo.objects.filter(num=num).first()
        if book:
            new=MyCollect.objects.filter(username=name,num=book.num)
            if new:
                pass
            else:
                MyCollect.objects.create(username=name,num=book.num,name=book.name,price=book.price,ISBN=book.ISBN,author=book.author,publisher=book.publisher,img=book.img,website=book.website,sales=book.sales)
        return HttpResponseRedirect('/query/?name='+bookname)
    


def rank(request):
    if request.method == 'GET':
        sql="select * from cmdb.cmdb_best_seller as A left join cmdb.cmdb_bookinfo as B on A.num = B.num order by A.id"
        try:
            books=get_data(sql)
        except:
            print("数据库连接失败：")
        
        
        #return HttpResponse(books[0][1])
        return render(request, 'rank.html',{'books':books})
def collect(request):
    if request.method == 'GET':
        name = request.session.get('name')
        books=MyCollect.objects.filter(username=name)
        i=1
        for book in books:
            book.i=i
            i+=1
        return render(request,"collect.html",{"books":books})

    
def usermanage_delete(request):
    id=request.GET.get("id")
    UserModel.objects.filter(id=id).delete()
    return HttpResponseRedirect("/usermanage/")
def collect_delete(request):
    id=request.GET.get("id")
    name = request.session.get('name')
    MyCollect.objects.filter(num=id,username=name).delete()
    return HttpResponseRedirect("/collect/")
def usermanage(request):
    if request.method == 'GET':
        users=UserModel.objects.all()
        return render(request,"user-manage.html",{'users':users})
    if request.method == "POST":
        if "adduser" in request.POST:
            username = request.POST.get('username1',None)
            password=request.POST.get('password',None)
            userModel = UserModel.objects.filter(username=username, password=password).first()
            if userModel:
                hint="账号密码已存在!"
                users=UserModel.objects.all()
                return render(request,"user-manage.html",{'hint':hint,'users':users})
            else:
                UserModel.objects.create(username=username,password=password)
                users=UserModel.objects.all()
                return render(request,"user-manage.html",{'users':users})
        

        
            

