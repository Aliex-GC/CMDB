"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from cmdb import views
urlpatterns = [
    path('index/', views.index),
    path('login/', views.login),
    path('register/', views.register),
    path('rank/', views.rank),
    path('query/', views.query),
    path('collect/', views.collect),
    path('collect/delete/', views.collect_delete),
    path('usermanage/',views.usermanage),
    path('usermanage/delete/',views.usermanage_delete),
    path('query/book_details/',views.qurey_book_details),
    path('query/collect/',views.query_collect),
    
]
