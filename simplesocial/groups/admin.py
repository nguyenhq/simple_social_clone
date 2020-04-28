from django.contrib import admin
from . import models
from groups.models import Group
# Register your models here.
# Inlines Nous voulons pouvoir créer des déclinaisons de groupmember directement sur la fiche
class GroupMemberInline(admin.TabularInline):
    model = models.GroupMember


class GroupAdmin(admin.ModelAdmin):
    model = Group
    list_display = ('id','description','name')
    # def get_member(self,obj):
    #     return obj.GroupMember.user
    # get_member.admin_order_field ='member'
    # get_member.short_description ='name member'
admin.site.register(models.GroupMember)
admin.site.register(models.Group,GroupAdmin)
