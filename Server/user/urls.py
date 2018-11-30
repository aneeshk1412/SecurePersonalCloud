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
from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from django.conf.urls.static import static
from . import views
from django.conf import settings

app_name = 'user'

urlpatterns = [
    path('list/', views.DirFileList.as_view(), name='dir_file_list'),
    path('datalist/', views.DirFileDataList.as_view(), name='dir_file_data_list'),
    path('status/<path:dir_path>', views.DirStatus.as_view(), name='dir_status'),
    path('details/<path:file_path>', views.DirFileDetail.as_view(), name='dir_file_view'),
    path('data/<path:file_path>', views.DirFileData.as_view(), name='dir_file_data_view'),
    # path('users/', views.UserList.as_view()),
    path('userdata/', views.UserDetail.as_view()),
    path('', views.user_home, name='user_home'),
    path('tree/', views.tree_view, name='tree_view'),
    path('<int:pk>/', views.dir_view, name='dir_view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


urlpatterns = format_suffix_patterns(urlpatterns)
