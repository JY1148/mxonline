from datetime import datetime

from django.db import models

from apps.users.models import BaseModel
from apps.organizations.models import Teacher
from apps.organizations.models import CourseOrg
from DjangoUeditor.models import UEditorField
"""
#设计表结构注意事项：
1. 表结构基础逻辑：实体1 ---<关系>--- 实体2 (一对多、多对多、多对一）
2. 表结构实体：课程Course 章节Lesson 视频Video 课程资源CourseResource
3. 实体的具体字段
4. 每个字段的类型，是否必填
"""


class Course(BaseModel):
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, verbose_name="讲师")#外键的引入，不可以跨文档进行（Teacher字段在organizations\models.py中，需要from import
    course_org = models.ForeignKey(CourseOrg, null=True, on_delete=models.CASCADE, verbose_name="机构")
    name = models.CharField(verbose_name="课程名",max_length=50)
    desc = models.CharField(verbose_name="课程描述",max_length=300)
    learn_times = models.CharField(default=0, verbose_name="学习时长（分钟数）", max_length=50)#尽管是数字，但IntegerField不支持max_length
    degree = models.CharField(verbose_name="难度", choices=(("pr", "初级"), ("me", "中级"), ("su", "高级")), max_length=2)
    students = models.IntegerField(default=0, verbose_name='学习人数')
    fav_nums = models.IntegerField(default=0, verbose_name='收藏人数')
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    notice = models.CharField(verbose_name="课程公告", max_length=300, default="")
    category = models.CharField(default=u"后端开发", max_length=20, verbose_name="课程类别")
    tag = models.CharField(default="", verbose_name="课程标签", max_length=10)
    youneed_know = models.CharField(default="", max_length=300, verbose_name="课程须知")
    teacher_tell = models.CharField(default="", max_length=300, verbose_name="老师告诉你")
    is_classics = models.BooleanField(default=False, verbose_name="是否经典")
    is_banner = models.BooleanField(default=False, verbose_name="是否广告位")

    detail = UEditorField(verbose_name="课程详情",width=600, height=300, imagePath="courses/ueditor/images/",
                          filePath="course/ueditor/files/", default="")
    image = models.ImageField(upload_to="courses/%Y/%m", verbose_name="封面图", max_length=100)

    class Meta:
        verbose_name = "课程信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def lesson_nums(self):
        return self.lesson_set.all().count()

    def show_image(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<img src='{}'>".format(self.image.url))
    show_image.short_description = "picture"

    def go_to(self):
        from django.utils.safestring import mark_safe
        return mark_safe("<a href='/course/{}'>跳转</a>".format(self.id))
    go_to.short_description = "跳转"

class BannerCourse(Course):
    class Meta:
        verbose_name = "轮播课程"
        verbose_name_plural = verbose_name
        proxy = True#有了这个migrations就不会重新新增一张表，我们只是希望多个管理器管理同一个数据

class CourseTag(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    tag = models.CharField(max_length=100, verbose_name="标签")

    class Meta:
        verbose_name = "课程标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag

class Lesson(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)#on_delete对应的外键数据（这里指Course)被删除后，当前的数据应该怎么办
    name = models.CharField(verbose_name=u"章节名",max_length=100)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    class Meta:
        verbose_name = "课程章节"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Video(BaseModel):
    lesson = models.ForeignKey(Lesson, verbose_name="章节", on_delete=models.CASCADE)
    name = models.CharField(verbose_name=u"视频名", max_length=100)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    url = models.CharField(max_length=1000, verbose_name=u"访问地址")
    class Meta:
        verbose_name = "视频"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class CourseResource(BaseModel):
    course = models.ForeignKey(Course, on_delete=models.CASCADE, verbose_name="课程")
    name = models.CharField(max_length=100, verbose_name=u"名称")
    file = models.FileField(upload_to="course/resourse/%Y/%m", verbose_name="下载地址", max_length=200)

    class Meta:
        verbose_name = "课程资源"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name