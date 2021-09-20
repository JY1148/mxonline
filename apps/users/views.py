from django.shortcuts import render
from django.views.generic.base import View
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from apps.users.forms import LoginForm, UploadImageForm, UserInfoForm,ChangePwdForm
from django.contrib.auth.mixins import LoginRequiredMixin
from apps.operations.models import UserFav, UserMessage,Banner
from apps.organizations.models import CourseOrg, Teacher
from apps.courses.models import Course
from pure_pagination import Paginator, PageNotAnInteger

# class CustomAuth(ModelBackend):
#     def authenticate(self, request, username=None, password=None, **kwargs):
#         try:
#             user=UserProfile.objects.get(Q(username=username)|Q(mobile=username))
#             if user.check_password(password):
#                 return user
#         except Exception as e:
#             return None



def message_nums(request):
    if request.user.is_authenticated:
        return {'unread_nums': request.user.usermessage_set.filter(has_read=False).count()}
    else:
        return {}

class MyMessageView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        messages = UserMessage.objects.filter(user=request.user)
        current_page = "messages"
        for message in messages:
            message.has_read = True
            message.save()

        # 对讲师列表进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(messages, per_page=2, request=request)
        messages = p.page(page)

        return render(request, "usercenter-message.html",{
            "messages" : messages,
            "current_page" : current_page
        })


class MyFavCourseView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavcourse"
        course_list = []
        fav_courses = UserFav.objects.filter(user=request.user, fav_type=1)
        for fav_course in fav_courses:
            try:
                course = Course.objects.get(id=fav_course.fav_id)
                course_list.append(course)
            except Course.DoesNotExist as e:
                pass
        return render(request, "usercenter-fav-course.html", {
            "course_list": course_list,
            "current_page": current_page
        })




class MyFavTeacherView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavteacher"
        teacher_list = []
        fav_teachers = UserFav.objects.filter(user=request.user, fav_type=3)
        for fav_teacher in fav_teachers:
            teacher = Teacher.objects.get(id=fav_teacher.fav_id)
            teacher_list.append(teacher)

        return render(request, "usercenter-fav-teacher.html",{
            "teacher_list": teacher_list,
            "current_page": current_page
        })

class MyFavOrgView(LoginRequiredMixin,View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "myfavorg"
        org_list = []
        fav_orgs = UserFav.objects.filter(user=request.user, fav_type=2)
        for fav_org in fav_orgs:
            org = CourseOrg.objects.get(id=fav_org.fav_id)
            org_list.append(org)

        return render(request, "usercenter-fav-org.html",{
            "org_list": org_list,
            "current_page": current_page
        })

class MyCourseView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "mycourse"
        # my_courses = UserCourses.objects.filter(user=request.user)
        return render(request, "usercenter-mycourse.html",{
            # "my_courses": my_courses,
            "current_page":current_page
        })

class ChangePwdView(View):
    login_url = "/login/"

    def post(self, request, *args, **kwargs):
        pwd_form = ChangePwdForm(request.POST)
        if pwd_form.is_valid():
            # pwd1 = request.POST.get("password1", "")
            # pwd2 = request.POST.get("password2", "")
            #
            # if pwd1 != pwd2:
            #     return JsonResponse({
            #         "status":"fail",
            #         "msg":"两次密码不一样哦"
            #     })
            pwd1 = request.POST.get("password1", "")
            user = request.user
            user.set_password(pwd1)
            user.save()
            # login(request,user)

            return JsonResponse({
                "status":"success"
            })
        else:
            return JsonResponse(pwd_form.errors)


class UploadImageView(LoginRequiredMixin, View):
    login_url = "/login/"

    # def save_file(self, file):
    #     with open("C:/Users/dell/PycharmProjects/MxOnline/media/head_image/uploaded.jpg", "wb") as f:
    #         for chunk in file.chunks():
    #             f.write(chunk)

    def post(self, request, *args, **kwargs):
        # 处理前端传来的用户头像
        image_form = UploadImageForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse({
                "status": "fail"
            })

        # files = request.FILES["image"]
        # self.save_file(files)


class UserInfoView(LoginRequiredMixin, View):
    login_url = "/login/"

    def get(self, request, *args, **kwargs):
        current_page = "info"
        return render(request, "usercenter-info.html", {
            "current_page": current_page
        })

    def post(self, request, *args, **kwargs):
        user_info_form = UserInfoForm(request.POST, instance=request.user)
        if user_info_form.is_valid():
            user_info_form.save()
            return JsonResponse({
                "status": "success"
            })
        else:
            return JsonResponse(user_info_form.errors)


class LogoutView(View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse("index"))  # 如果用户已登录，哪怕输入login页面也跳转到index页面


class LoginView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse("index"))  # 如果用户已登录，哪怕输入login页面也跳转到index页面

        banners = Banner.objects.all()[:3]
        next = request.GET.get("next", "")
        return render(request, "login.html", {
            "next": next,
            "banners":banners
        })

    def post(self, request, *args, **kwargs):
        banners = Banner.objects.all()[:3]
        # 判断账号密码是否存在未填写状态之方法一if
        # user_name = request.POST.get("username", "")
        # password = request.POST.get("password", "")
        # if not user_name:
        #     return render(request, "login.html", {"msg": "请输入用户名"})
        # if not password:
        #     return render(request, "login.html", {"msg": "请输入密码"})
        # if len(password) < 3:
        #     return render(request, "login.html", {"msg": "密码格式不正确"})

        # 判断账号密码是否存在未填写状态之方法二表单验证
        login_form = LoginForm(request.POST)

        if login_form.is_valid():

            # 用于通过用户和密码查询是否存在
            user_name = login_form.cleaned_data["username"]
            password = login_form.cleaned_data["password"]
            user = authenticate(username=user_name, password=password)
            # 不用UserProfile的原因是UserProfile中的密码是加密存储的
            # from apps.users.models import UserProfile
            # user = UserProfile.objects.get(username=user_name, password=password)
            if user is not None:
                # 查询到用户
                login(request, user)
                # 登录成功之后返回页面
                # 在某课程入口又跳转回首页很麻烦，怎么办
                next = request.GET.get("next", "")
                if next:
                    return HttpResponseRedirect(next)
                return HttpResponseRedirect(reverse("index"))
            else:
                # 未查询到用户

                return render(request, "login.html", {
                    "msg": "用户名或密码错误",
                    "login_form": login_form,
                    "banners":banners
                })
        else:
            return render(request, "login.html", {
                "login_form": login_form,
                "banners": banners,
            })
