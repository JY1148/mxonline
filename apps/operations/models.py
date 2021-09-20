from django.db import models

from django.contrib.auth import get_user_model

from apps.users.models import BaseModel #之所以不在users.models里引入UserProfile而是改用import get_user_model：用自带的覆盖django的表，避免后期直接使用django自带的user表改动大的问题
from apps.courses.models import Course

UserProfile = get_user_model()

class Banner(BaseModel):
    title = models.CharField(max_length=100, verbose_name="标题")
    image= models.ImageField(upload_to="banner%Y/%m", max_length=200, verbose_name="轮播图")
    url = models.URLField(max_length=200, verbose_name="访问地址")
    index= models.IntegerField(default=0, verbose_name="顺序")

    class Meta:
        verbose_name = "轮播图"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title

class UserAsk(BaseModel):
    name = models.CharField(max_length=20, verbose_name=u"姓名")
    mobile = models.CharField(max_length=11, verbose_name="手机")
    course_name = models.CharField(max_length=50, verbose_name="课程名")

    class Meta:
        verbose_name = "用户查询"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{name}_{course}({mobile})".format(name = self.name, course= self.course_name, mobile = self.mobile)

class CourseComments(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    comment = models.CharField(max_length=200, verbose_name="评论内容")

    class Meta:
        verbose_name = "课程评论"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.comment

class UserFav(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    # course = models.ForeignKey(Course, verbose_name="课程")
    # teacher = models.ForeignKey(Teacher, verbose_name="讲师")
    #这种做法，每当有新增收藏项目又要新增一列，相对浪费：列越来越多，外键越来越多
    fav_id = models.IntegerField(verbose_name="数据id")
    fav_type = models.IntegerField(choices=((1,"课程"),(2,"课程机构"),(3,"讲师")),default=1, verbose_name="收藏类型")

    class Meta:
        verbose_name = "用户收藏"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "{user}_{id}".format(user=self.user.username, id=self.fav_id)#返回显示的内容是“字符串”；字符串中包含表，表的指代在小括号中说明


class UserMessage(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, verbose_name="用户")
    message = models.CharField(max_length=200, verbose_name="消息内容")
    has_read = models.BooleanField(default=False,verbose_name="是否已读")

    class Meta:
        verbose_name = "用户消息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.message

class UserCourses(BaseModel):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE,  verbose_name="用户")
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")

    class Meta:
        verbose_name = "用户课程"
        verbose_name_plural = verbose_name


    def __str__(self):
        return self.course.name