from django.db import models
from django.utils.text import slugify
# from django.conf import settings #?
from django.urls import reverse
# Create your models here.
# installing the c++ Compiler for python with this command:
# conda install libpython m2w64-toolchain -c msys2
# pip install misaka
import misaka # It features a fast HTML renderer and functionality to make custom renderers

from django.contrib.auth import get_user_model # call User's model of Django
User = get_user_model()

# https://docs.djangoproject.com/en/2.0/howto/custom-template-tags/#inclusion-tags
# This is for the in_group_members check template tag
#https://openclassrooms.com/fr/courses/1871271-developpez-votre-site-web-avec-le-framework-django/1873273-simplifions-nos-templates-filtres-tags-et-contextes
from django import template
register = template.Library() #?? custom template may be <p class="mb-1">{{ group.description_html|safe }}</p>

class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default ='')
    description_html = models.TextField(editable=False, blank=True, default='')
    members = models.ManyToManyField(User,through="GroupMember") # Ajout member here when relationship m2m, why not ajout this in Model "User", but is complicated

    def __str__(self):
        return self.name
# Overriding predefined model methods
# model có nhiều các method được dựng sẵn của Django và trong đó hiển nhiên sẽ có các method là sự thể hiện các hành vi vơi cơ sở dữ liệu. Thông thường thì chúng ta sẽ muốn tùy chỉnh các hành vi save() hay delete()
#
# Và đương nhiên là chũng ta hoàn toàn có thể làm được điều này bằng cách override lại chính method đó. Cụ thể như sau:
    def save(self,*args,**kwargs):
        self.slug = slugify(self.name) #sesion previous
        self.description_html =misaka.html(self.description)
        super().save(*args,**kwargs) # Call the "real" save() method.

    def get_absolute_url(self): #method này cho phép Django có thể biết được cách biết được URL cho từng object. Mặc định thf Django sẽ sử dụng nó trong admin interface
        return reverse('groups:single',kwargs={'slug': self.slug})

    class Meta:
        ordering   = ['name']

class GroupMember(models.Model):
    group = models.ForeignKey(Group,related_name='memberships',on_delete=models.CASCADE)
    user = models.ForeignKey(User,related_name='user_groups', on_delete = models.CASCADE)

    def __str__(self):
        return self.user.username

    class Meta:
        unique_together =("group","user")
#############################################
#         test for understanding
# python manage.py shell
# from groups.models import Group,GroupMember
#  print(Group.objects.all())
#  group1=Group.objects.get(name="Google3")
#  group1.members
