from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import CreateView
from . import forms

# CreateView should be used when you need a form on the page
# and need to do a db insertion on submission of a valid form.
# CreateView is better than  View
class SignUp(CreateView):
    form_class = forms.UserCreateFrom
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'
