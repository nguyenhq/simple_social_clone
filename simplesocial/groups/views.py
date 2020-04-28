# from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import(
    LoginRequiredMixin,
    PermissionRequiredMixin
)
from django.views.generic import(TemplateView,ListView,
                                    DetailView,CreateView,UpdateView,DeleteView)
from django.views import generic
from django.urls import reverse
from django.db import IntegrityError
from groups.models import Group, GroupMember
from . import models

# Create your views here.
class CreateGroup(LoginRequiredMixin,CreateView):
    fields = ("name","description")
    model = Group

class SingleGroup(DetailView):
    model = Group
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context["one_user"] = self.model.objects.filter(members=1)
    #     return context

class ListGroup(ListView):
    model = Group

class JoinGroup(LoginRequiredMixin,generic.RedirectView):
    def get_redirect_url(self,*args,**kwargs):
        return reverse('groups:single', kwargs={'slug':self.kwargs.get('slug')})

    def get(self, request, *args, **kwargs):
        group = get_object_or_404(Group,slug=self.kwargs.get("slug"))
        try:
            GroupMember.objects.create(user=self.request.user,group=group)
        except IntegrityError:
            messages.warning(self.request,("# WARNING: , already a member of {}".format(group.name)))
        else:
            messages.success(self.request,"You are now a member of the {}".format(group.name))
        return super().get(request, *args,**kwargs)

class LeaveGroup(LoginRequiredMixin,generic.RedirectView):
    def get(self,request, *args, **kwargs):
        try:
            membership = models.GroupMember.objects.filter(
                user=self.request.user,
                group__slug=self.kwargs.get("slug")
            ).get()

        except models.GroupMember.DoesNotExist:
            messages.warning(
                self.request, "You can't leave this group because you aren't in it"
            )

        else:
            membership.delete()
            messages.success(
                self.request,
                "You have successfully left this group."
            )
        return super().get(request, *args, **kwargs)

    def get_redirect_url(self, *args, **kwargs):
        return reverse("groups:single", kwargs={"slug": self.kwargs.get("slug")})
