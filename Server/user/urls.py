"""Server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from rest_framework.urlpatterns import format_suffix_patterns
from . import views
from django.conf.urls import include

urlpatterns = [
    path('list/', views.DirFileList.as_view(), name='dir_file_list'),
    path('details/<path:file_path>', views.DirFileDetail.as_view(), name='dir_file_view'),
    path('users/', views.UserList.as_view()),
    path('user/<str:username>/', views.UserDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
