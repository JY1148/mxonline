from django.db import models

from apps.users.models import BaseModel
from apps.users.models import UserProfile
from DjangoUeditor.models import UEditorField

"""
#设计表结构注意事项：
1. 表结构基础逻辑：实体1 ---<关系>--- 实体2 (一对多、多对多、多对一）
2. 表结构实体：课程Course 章节Lesson 视频Video 课程资源CourseResource
3. 实体的具体字段
4. 每个字段的类型，是否必填
"""

class City(BaseModel):#本来属于课程机构下的标签属性“城市”,由于在后期可能会添加新变量，因此单独做出一个新字段。而“城市”也成为了“课程机构”的外部字段
    name = models.CharField(max_length=10, verbose_name=u"城市")
    desc = models.CharField(max_length=20, verbose_name=u"描述")
    class Meta:
        verbose_name = "城市"
        verbose_name_plural = verbose_name

#当创建城市的时候,会在前端页面出现城市”上海“创建成功
    def __str__(self):
        return self.name


class CourseOrg(BaseModel):
    name = models.CharField(max_length=50, verbose_name="机构名称")
    desc = UEditorField(verbose_name="机构详情",width=600, height=300, imagePath="courses/ueditor/images/",
                          filePath="course/ueditor/files/", default="")
    tag = models.CharField(default="全国知名", max_length=10, verbose_name="机构标签")
    category = models.CharField(default="pxjg", verbose_name=u"机构类别", max_length=4, choices=(("pxjg","培训机构"),("gr","个人"),("gx","高校")))
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    image = models.ImageField(upload_to="org/%Y/%m", verbose_name=u"logo", max_length=100)
    address = models.CharField(max_length=150, verbose_name="机构地址")
    students = models.IntegerField(default=0, verbose_name="学习人数")
    course_nums = models.IntegerField(default=0, verbose_name="课程数")
    city = models.ForeignKey(City, on_delete=models.CASCADE, verbose_name="所在城市")
    is_auth = models.BooleanField(default=False, verbose_name="是否认证")
    is_gold = models.BooleanField(default=False, verbose_name="是否金牌")

    def courses(self):#便于在html中直接调用，就不用直接在views.py中引入
        # from apps.courses.models import Course #这个import不能作为全局引入，因为在courses的models.py中有引入本models.py的CourseOrg,出现循环引入。而写在这里的调用属于动态属性（调用的时候才会执行）
        # course = Course.objects.filter(course_org = self)
        courses = self.course_set.filter(is_classics=True)[:3]#该方法用到course_set.all不需引入，更加不易出错，完成数据反向取
        return courses

    class Meta:
        verbose_name = "课程机构"
        verbose_name_plural = verbose_name

#当创建城市的时候,会在前端页面出现机构”新东方“创建成功
    def __str__(self):
        return self.name

class Teacher(BaseModel):
    user=models.OneToOneField(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    org = models.ForeignKey(CourseOrg, on_delete=models.CASCADE, verbose_name="所属机构")
    name = models.CharField(max_length=50, verbose_name=u"教师名")
    work_years = models.IntegerField(default=0, verbose_name="工作年限")
    work_company = models.CharField(max_length=50, verbose_name="就职公司")
    work_position = models.CharField(max_length=50, verbose_name="公司职位")
    points = models.CharField(max_length=50, verbose_name="教学特点")
    click_nums = models.IntegerField(default=0, verbose_name="点击数")
    fav_nums = models.IntegerField(default=0, verbose_name="收藏数")
    age = models.IntegerField(default=18, verbose_name="年龄")
    image = models.ImageField(upload_to="teacher/%Y/%m", verbose_name="头像", max_length=100)

    class Meta:
        verbose_name = "课程讲师"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

    def course_nums(self):
        return self.course_set.all().count()