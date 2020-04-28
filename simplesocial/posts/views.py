from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
# Create your views here.
# SelectRelatedMixin
# A simple mixin which allows you to specify a list or tuple of foreign key fields to perform a select_related on
# pip install django-braces
from braces.views import SelectRelatedMixin
from django.views import generic # call CRUD

from . import forms
from . import models
# Don't forget to import the model
from groups.models import Group

from django.contrib.auth import get_user_model
User = get_user_model()

class PostList(SelectRelatedMixin,generic.ListView):
    model = models.Post
    select_related = ('user','group') # If you don't set the select_related class attribute it ultimately has not effect on the class.
    queryset=models.Post.objects.all()

    def get_context_data(self, **kwargs):

         context = super(PostList, self).get_context_data(**kwargs)
         context['user_groups'] = Group.objects.filter(members__in=[self.request.user])
         context['all_groups'] = Group.objects.all()
         return context

class UserPosts(generic.ListView):
    model = models.Post
    template_name = 'posts/user_post_list.html'
#  3 method get data: get,get_queryset, get_context_data () important()
    def get_queryset(self):
        try:
            # Tim bai "Tối ưu hóa queryset với select_related và prefetch_related"
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username") # And then we're going to get the user name is exactly equal to the user name of whatever is user logged
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return   self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context

class PostDetail(SelectRelatedMixin,generic.DetailView):
    model = models.Post
    select_related = ("user","group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username") # note: Do not use request.user without login check
        )
#  question: How come CreatePost in SimpleSocial has form_valid function but CreatePost in blog doesn't? They both have a user associated with it. And there isn't anything else being done in form_valid function in SimpleSocial.
# answer This is really a question of design. They are just different approaches to similar issues and neither of them is right nor wrong. In the Blog project when we create a post we have to manually select a value for the  author field. In the SimpleSocial project by adding the form_valid method we set the author (now called user) to a property from the incoming request so that user is always set to whoever is actually creating the post.
class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    form_class = forms.PostForm
    # fields = ('message','group')
    model = models.Post
    # fields["group"].queryset = models.Group.objects.filter(members = object.user)

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs.update({"user": self.request.user})
        return kwargs

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin,SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ('user','group')
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self,*args,**kwargs):
        messages.success(self.request,"post deleted")
        return super().delete(*args,**kwargs)
