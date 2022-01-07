from django.contrib.auth.views import LoginView
from django.shortcuts import render


# Create your views here.
class LoginListView(LoginView):
    template_name = 'authapp/login.html'
