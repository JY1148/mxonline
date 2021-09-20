from django.shortcuts import render
from django.views.generic import View
from django.http import JsonResponse

from apps.operations.forms import UserFavForm, CommentsForm #表单
from apps.operations.models import UserFav, CourseComments, Banner
from apps.courses.models import Course
from apps.organizations.models import CourseOrg, Teacher

class IndexView(View):
    def get(self, request, *args, **kwargs):
        banners = Banner.objects.all().order_by("index")
        courses = Course.objects.filter(is_banner=False)[:6]
        banner_courses = Course.objects.filter(is_banner=True)
        course_orgs = CourseOrg.objects.all()[:15]
        #return的内容是给前端html使用的
        return render(request, "index.html",{
            "banners":banners,
            "courses":courses,
            "banner_courses":banner_courses,
            "course_orgs":course_orgs
        })

class CommentView(View):
    def post(self, request, *args, **kwargs):
        #用户收藏
        #用户取消收藏
        #如果用户未登录，给前端返回数据：状态失败，信息用户未登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        comment_form = CommentsForm(request.POST)
        if comment_form.is_valid():
            course = comment_form.cleaned_data["course"]
            comments = comment_form.cleaned_data["comment"]#”comment"是基于CourseComments里面的一个charfield

            comment = CourseComments()
            comment.user = request.user
            comment.comment = comments#comments只是一个名称，对应comment_form.cleaned_data["comment"]
            comment.course = course
            comment.save()

            return JsonResponse({
                 "status": "success",
            })
        else:
            return JsonResponse({
                 "status": "fail",
                "msg": "参数错误"
            })

class AddFavView(View):
    def post(self, request, *args, **kwargs):
        #用户收藏
        #用户取消收藏
        #如果用户未登录，给前端返回数据：状态失败，信息用户未登录
        if not request.user.is_authenticated:
            return JsonResponse({
                "status": "fail",
                "msg": "用户未登录"
            })

        userfav_form = UserFavForm(request.POST) #表单实例化
        if userfav_form.is_valid():
            fav_id = userfav_form.cleaned_data["fav_id"]
            fav_type = userfav_form.cleaned_data["fav_type"]

            #验证收藏是否存在
            existed_records = UserFav.objects.filter(user=request.user, fav_id=fav_id, fav_type=fav_type)
            if existed_records:
                existed_records.delete()

                if fav_type == 1:
                    course = Course.objects.get(id=fav_id)
                    course.fav_nums -= 1
                    course.save()
                elif fav_type == 2:
                    course_org = CourseOrg.objects.get(id=fav_id)
                    course_org.fav_nums -= 1
                    course_org.save()
                elif fav_type == 3:
                    teacher = Teacher.objects.get(id=fav_id)
                    teacher.fav_nums -= 1
                    teacher.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "收藏"
                })
            else:
                user_fav = UserFav()
                user_fav.fav_id = fav_id
                user_fav.fav_type = fav_type
                user_fav.user = request.user
                user_fav.save()

                return JsonResponse({
                    "status": "success",
                    "msg": "收藏好了"
                })
        else:
            return JsonResponse({
                "status": "fail",
                "msg": "请重试一次"
            })