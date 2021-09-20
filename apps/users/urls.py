from django.conf.urls import url
from apps.users.views import UserInfoView, UploadImageView, ChangePwdView, MyCourseView,MyFavOrgView,MyFavTeacherView,MyFavCourseView,MyMessageView
from apps.users.views import MyCourseView
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(),name="info"),
    url(r'^image/upload/$', UploadImageView.as_view(),name="image"),
    url(r'^update/pwd/$', ChangePwdView.as_view(),name="update_pwd"),
    # url(r'^mycourse/$', MyCourseView.as_view(),name="mycourse"),
    # 不用自己新建view↑，用已存在的templateview↓（同时添加login_required,current-page)
    url(r'^mycourse/$', login_required(TemplateView.as_view(template_name="usercenter-mycourse.html"), login_url= "/login/"),{"current_page":"mycourse"},name="mycourse"),
    url(r'^myfavorg/$', MyFavOrgView.as_view(), name="myfavorg"),
    url(r'^myfavteacher/$', MyFavTeacherView.as_view(), name="myfavteacher"),
    url(r'^myfavcourse/$', MyFavCourseView.as_view(), name="myfavcourse"),
    url(r'^messages/$', MyMessageView.as_view(), name="messages"),
]