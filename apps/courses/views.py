from django.shortcuts import render
from django.views.generic.base import View
from pure_pagination import Paginator, PageNotAnInteger
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q


from apps.courses.models import Course, CourseTag, CourseResource, Video#引入课程信息
from apps.operations.models import UserFav, UserCourses, CourseComments

class VideoView(LoginRequiredMixin, View):
    login_url = "/login/"#去哪里登录，给未登录的跳转
    def get(self, request, course_id, video_id, *args, **kwargs):
        """获取课程章节信息"""
        course = Course.objects.get(id=int(course_id))
        course.click_nums +=1
        course.save()

        video = Video.objects.get(id=int(video_id))

        #查询用户是否已关联该课程
        user_courses = UserCourses.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        #学习过该课程的同学
        user_courses = UserCourses.objects.filter(course= course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourses.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:3]#user_ids是个列表
        #related_courses = [user_course.course for user_course in all_courses if user_courses.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-play.html",{
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "video": video,

        })

class CourseCommentsView(LoginRequiredMixin, View):
    login_url = "/login/"#去哪里登录，给未登录的跳转
    def get(self, request, course_id, *args, **kwargs):
        course = Course.objects.get(id=int(course_id))
        course.click_nums +=1
        course.save()

        comments = CourseComments.objects.filter(course=course)

        #查询用户是否已关联该课程
        user_courses = UserCourses.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        # 学习过该课程的同学
        user_courses = UserCourses.objects.filter(course=course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourses.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[
                      :3]  # user_ids是个列表
        # related_courses = [user_course.course for user_course in all_courses if user_courses.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-comment.html", {
            "course": course,
            "course_resources": course_resources,
            "related_courses": related_courses,
            "comments": comments,

        })


class CourseLessonView(LoginRequiredMixin, View):
    login_url = "/login/"#去哪里登录，给未登录的跳转
    def get(self, request, course_id, *args, **kwargs):
        """获取课程章节信息"""
        course = Course.objects.get(id=int(course_id))
        course.click_nums +=1
        course.save()

        # 1.学习用户与课程之间的关联
        # 2.对view进行login登录的验证
        # 3.其他课程推荐

        #查询用户是否已关联该课程
        user_courses = UserCourses.objects.filter(user=request.user, course=course)
        if not user_courses:
            user_course = UserCourses(user=request.user, course=course)
            user_course.save()

            course.students += 1
            course.save()

        #学习过该课程的同学
        user_courses = UserCourses.objects.filter(course= course)
        user_ids = [user_course.user.id for user_course in user_courses]
        all_courses = UserCourses.objects.filter(user_id__in=user_ids).order_by("-course__click_nums")[:3]#user_ids是个列表
        #related_courses = [user_course.course for user_course in all_courses if user_courses.id != course.id]
        related_courses = []
        for item in all_courses:
            if item.course.id != course.id:
                related_courses.append(item.course)

        course_resources = CourseResource.objects.filter(course=course)

        return render(request, "course-video.html",{
            "course" : course,
            "course_resources": course_resources,
            "related_courses": related_courses,

        })



class CourseDetailView(View):
    def get(self, request, course_id, *args, **kwargs):
        """获取课程详情"""
        course = Course.objects.get(id=int(course_id))
        course.click_nums +=1
        course.save()

        #获取收藏状态
        has_fav_course = False
        has_fav_org = False
        if request.user.is_authenticated:
            if UserFav.objects.filter(user=request.user, fav_id=course_id, fav_type=1):
                has_fav_course = True
            if UserFav.objects.filter(user=request.user, fav_id=course_id, fav_type=2):
                has_fav_org = True


        #通过课程的单一tag做课程推荐
        # tag = course.tag
        # related_courses = []
        # if tag:
        #     related_courses = Course.objects.filter(tag=tag).exclude(id=course.id)[:3]

        # 通过课程的多个tag做课程推荐
        tags = course.coursetag_set.all()
        # tag_list=[]
        # for tag in tags:
        #     tag_list.append(tag.tag)
        tag_list = [tag.tag for tag in tags]

        course_tags = CourseTag.objects.filter(tag__in=tag_list).exclude(course__id=course.id)
        related_courses = set() #用[]也可以，不过会有重复值，下面的方法就不是add而是append
        for course_tag in course_tags:
            related_courses.add(course_tag.course)

        return render(request, "course-detail.html",{
            "course" : course,
            "has_fav_course": has_fav_course,
            "has_fav_org": has_fav_org,
            "related_courses": related_courses,

        })

class CourseListView(View):
    def get(self, request, *args, **kwargs):
        """获取课程列表信息"""
        #1.获取所有课程
        #all_courses = Course.objects.all()
        #2.将所有课程排序
        all_courses = Course.objects.order_by("-add_time")
        hot_courses = Course.objects.order_by("-click_nums")[:3]

        keywords = request.GET.get("keywords","")
        s_type = "course"
        if keywords:
            all_courses = all_courses.filter(Q(name__icontains=keywords)|Q(desc__icontains=keywords)|Q(desc__icontains=keywords))

        #课程排序
        sort = request.GET.get("sort","")
        if sort == "students":
            all_courses = Course.objects.order_by("-students")
        elif sort == "hot":
            all_courses = Course.objects.order_by("-click_nums")

        # 对课程机构进行分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1
        p = Paginator(all_courses, per_page=2, request=request)
        courses = p.page(page)

        #3.传递课程网站,传递上面的变量进入网站
        return render(request, "course-list.html",{
            "all_courses": courses,
            "sort" : sort,
            "hot_courses" : hot_courses,
            "keywords":keywords,
            "s_type":s_type
        })

