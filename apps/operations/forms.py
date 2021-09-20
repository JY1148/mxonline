import re

from django import forms
from apps.operations.models import UserFav, CourseComments

#既有form的特性，又有model的特性
class UserFavForm(forms.ModelForm):
    class Meta:
        model = UserFav
        fields = ["fav_id", "fav_type"]

#表达认证
class CommentsForm(forms.ModelForm):
    class Meta:
        model = CourseComments
        fields = ["course", "comment"]