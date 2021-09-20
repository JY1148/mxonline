import xadmin
#将自己的model注册到xadmin之中（以本adminx为例，将之前生成的organizations下的相关models，引入相关model，进行配置）
from apps.organizations.models import Teacher, CourseOrg, City

#全局配置，可放在任一adminx中

class GlobalSettings(object):
    site_title = "一个后台管理系统"
    site_footer = "好极有限"
    #menu_style = "accordion"

class BaseSettings(object):
    enable_themes = True
    use_bootswatch = True

#注册表
class TeacherAdmin(object):
    list_display = ["id", "name"]
    search_fields = ["name"]
    list_filter = ["add_time", "name"]
    model_icon = 'fa fa-universal-access'
    readonly_fields = ["add_time"]

#给不同的键加以不同的xadmin功能，例如list_display呈现什么键，serach_fields可以搜索什么键的内容，list_filter可以在键下进行什么过滤；外键下的键用双下划线

class CourseOrgAdmin(object):
    list_display = ["id", "name", "desc"]
    search_fields = ["name", "desc"]
    list_filter = ["add_time", "name", "desc"]
    model_icon = 'fa fa-institution'
    readonly_fields = ["add_time"]
    style_fields ={
        "desc":"ueditor"
    }

class CityAdmin(object):
    list_display = ["id", "name", "desc"]
    search_fields = ["name", "desc"]
    list_filter = ["add_time", "name", "desc"]
    list_editable = ["name", "desc"]
    model_icon = 'fa fa-building'
    readonly_fields = ["add_time"]


#讲上面的class都注册到xadmin当中去
xadmin.site.register(Teacher, TeacherAdmin)
xadmin.site.register(CourseOrg, CourseOrgAdmin)
xadmin.site.register(City, CityAdmin)
#在xadmin中的views.py中的CommAdminView中注入上面的class：GlobalSettings
xadmin.site.register(xadmin.views.CommAdminView,GlobalSettings)
xadmin.site.register(xadmin.views.BaseAdminView,BaseSettings)