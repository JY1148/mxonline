import xadmin

from apps.courses.models import Course, Lesson, Video, CourseResource, CourseTag, BannerCourse
from xadmin.layout import Fieldset, Main, Side, Row
#注册表

class LessonInline(object):
    model= Lesson
    # style= "tab"
    extra = 0
    exclude = ["add_time"]

class CourseResourceInline(object):
    model= CourseResource
    style= "tab"
    extra = 1

class CourseAdmin(object):
    list_display = ["id", "name", "desc","degree", "learn_times", "students"]
    search_fields = ["name", "desc","degree", "students"]
    list_filter = ["add_time", "name", "desc","detail","degree", "learn_times","students"]
    list_editable = ["degree", "desc"]

class BannerCourseAdmin(object):
    list_display = ["id", "name", "desc","degree", "learn_times", "students"]
    search_fields = ["name", "desc","degree", "students"]
    list_filter = ["add_time", "name", "desc","detail","degree", "learn_times","students"]
    list_editable = ["degree", "desc"]
    model_icon = 'fa fa-star'

    def queryset(self):
        qs =super().queryset()
        qs = qs.filter(is_banner=True)
        return qs

from import_export import resources

class MyResource(resources.ModelResource):
    class Meta:
        model = Course
        # fields = ('name', 'description',)
        # exclude = ()

class NewCourseAdmin(object):
    import_export_args = {'import_resource_class': MyResource, 'export_resource_class': MyResource}
    list_display = ["id", "name", "desc","degree", "learn_times", "students", "go_to"]
    search_fields = ["name", "desc","degree", "students"]
    list_filter = ["add_time", "name", "desc","detail","degree", "learn_times","students"]
    list_editable = ["degree", "desc"]
    readonly_fields = ["click_nums", "fav_nums", "students","add_time"]
    exclude = []
    ordering = ["-click_nums"]
    model_icon = 'fa fa-address-book-o'
    inlines = [LessonInline, CourseResourceInline]
    style_fields ={
        "detail":"ueditor"
    }

    def queryset(self):
        qs =super().queryset()
        if not self.request.user.is_superuser:
            qs = qs.filter(teacher=self.request.user.teacher)
        return qs


    def get_form_layout(self):
        self.form_layout = (
            Main(
                Fieldset("讲师信息",
                         'teacher', 'course_org',
                         css_class='unsort no_title'
                         ),
                Fieldset("基本信息",
                         'name', 'desc',
                         Row('learn_times', 'degree'),
                         Row('category', 'tag'),
                         'youneed_know','teacher_tell','detail',
                         ),
            ),
            Side(
                Fieldset("课程特性",
                         'is_classics', 'is_banner',
                         ),
            ),
            Side(
                Fieldset("访问信息",
                         'fav_nums', 'click_nums',
                         'students', 'add_time',
                         ),
            )
        )
        return super(NewCourseAdmin, self).get_form_layout()


class LessonAdmin(object):
    list_display = ['course', 'name', 'add_time']
    search_fields = ['course', 'name']
    list_filter = ['course__name', 'name', 'add_time']#course__name是两个下划线的原因是外键；再外键的类型之下再作过滤
    model_icon = 'fa fa-book'
    readonly_fields = ["add_time"]



class VideoAdmin(object):
    list_display = ['lesson', 'name', 'add_time']
    search_fields = ['lesson', 'name']
    list_filter = ['lesson', 'name', 'add_time']
    model_icon = 'fa fa-file-video-o'
    readonly_fields = ["add_time"]



class CourseResourceAdmin(object):
    list_display = ['course', 'name', 'file', 'add_time']
    search_fields = ['course', 'name', 'file']
    list_filter = ['course', 'name', 'file', 'add_time']
    model_icon = 'fa fa-file-zip-o'
    readonly_fields = ["add_time"]

class CourseTagAdmin(object):
    list_display = ['course', 'tag', 'add_time']
    search_fields = ['course', 'tag']
    list_filter = ['course', 'tag', 'add_time']
    model_icon = 'fa fa-tags'
    readonly_fields = ["add_time"]


# xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(BannerCourse, BannerCourseAdmin)
xadmin.site.register(Course, NewCourseAdmin)
xadmin.site.register(Lesson, LessonAdmin)
xadmin.site.register(Video, VideoAdmin)
xadmin.site.register(CourseResource, CourseResourceAdmin)
xadmin.site.register(CourseTag, CourseTagAdmin)
