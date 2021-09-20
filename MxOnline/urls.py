"""MxOnline URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path #url比path要强大（支持正则表达时），而re_path也支持正则表达式
from django.conf.urls import url, include
from django.views.generic import TemplateView
from django.views.static import serve
from apps.operations.views import IndexView

import xadmin


from apps.users.views import LoginView, LogoutView

from MxOnline.settings import MEDIA_ROOT
urlpatterns = [
    #path('admin/', admin.site.urls),
#url知识：凡是含有xadmin/的路径，都经由xadmin.site.urls转发哪个方法上和处理
    path('xadmin/', xadmin.site.urls),
#之所以template_name不需要加集体的文件位置，主要是‘DIRS'：[os.path.join(BASE_DIR,'templates']
    path('',IndexView.as_view(), name="index"),
#login的斜线一定要加，不加子页面访问不了
#给url命名，后期更改更方便
    path('login/', LoginView.as_view(), name="login"),
    #配置富文本相关url
    url(r'^ueditor/',include('DjangoUeditor.urls')),
    path('logout/', LogoutView.as_view(), name='logout'),
    #机构相关页面
    url(r'^org/', include(('apps.organizations.urls',"organizations"), namespace="org")),
    #配置上传文件的访问url
    url(r'^media/(?P<path>.*)$', serve,{"document_root":MEDIA_ROOT}),#正则表达式：*将media后面所有的字符串取出，放入到path的变量名称之中，取出的变量传递给serve $结尾符
    #用户相关操作
    url(r'^op/', include(('apps.operations.urls',"operations"), namespace="op")),
    #课程相关页面
    url(r'^course/', include(('apps.courses.urls',"courses"), namespace="course")),
    # 用户个人中心
    url(r'^users/', include(('apps.users.urls', "users"), namespace="users")),

    #配置富文本相关的url
    url(r'^ueditor/', include('DjangoUeditor.urls')),
]

#1. CBV(class base view) 用class 与 FBV(function base view) 用函数
#class的好处在于可以继承