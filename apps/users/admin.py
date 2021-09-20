from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from apps.users.models import UserProfile

class UserProfileAdmin(admin.ModelAdmin):
    pass

# admin.site.register(UserProfile, UserAdmin)
# xadmin会自动发现UserProfile并注入，因此在注释化该代码后，xadmin依然顺利运行之前在admin注册的用户信息
# Register your models here.
