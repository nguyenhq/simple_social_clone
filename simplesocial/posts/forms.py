from django import forms
from . import models


class PostForm(forms.ModelForm):
    class Meta:
        fields = ("message", "group")
        model = models.Post

    def __init__(self, *args, **kwargs):
        user = kwargs.pop("user", None) # if user defined user is "user" else user = null
        super().__init__(*args, **kwargs) #https://www.udemy.com/course/python-and-django-full-stack-web-developer-bootcamp/learn/lecture/7133898#questions/3910688
        if user is not None:
            self.fields["group"].queryset = models.Group.objects.filter(members = user)

# models.Group.objects.filter(
#     pk__in=user.groups.values_list("group__pk") not working
