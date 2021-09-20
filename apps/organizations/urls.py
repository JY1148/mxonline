from django.conf.urls import url
from django.urls import path

from apps.organizations.views import OrgView, AddAskView, OrgHomeView, OrgTeacherView
from apps.organizations.views import OrgCourseView, OrgDescView, TeacherListView, TeacherDetailView
urlpatterns = [
    url(r'^list/$', OrgView.as_view(),name="list"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),
    url(r'^add_ask/$', AddAskView.as_view(), name="add_ask"),
    url(r'^(?P<org_id>\d+)/$', OrgHomeView.as_view(), name="home"),
    # path('<int:org_id>/', OrgHomeView.as_view(), name="home"), 用path方法同样可以调用OrgHomeView

    #讲师详情页
    url(r'^(?P<org_id>\d+)/teacher/$', OrgTeacherView.as_view(), name="teacher"),
    url(r'^(?P<org_id>\d+)/course/$', OrgCourseView.as_view(), name="course"),
    url(r'^(?P<org_id>\d+)/desc/$', OrgDescView.as_view(), name="desc"),
    #讲师列表页
    url(r'^teachers/$', TeacherListView.as_view(), name="teachers"),
    url(r'^teachers/(?P<teacher_id>\d+)/$',TeacherDetailView.as_view(), name="teacher_detail"),
]