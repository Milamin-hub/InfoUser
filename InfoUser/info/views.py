from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from info.forms import *
from info.models import Profile 
from django.shortcuts import render, redirect


class UserLoginView(LoginView):
    form = LoginForm()
    template_name = 'info/account/login.html'
    

class UserLogoutView(LogoutView):
    template_name = 'info/account/logout.html'


def user_profile(request):
    if request.user.is_authenticated:
        try:
            profile = Profile.objects.get(user=request.user)
            return render(request, 'info/account/user_profile.html', {'profile': profile})
        except:
            return render(request, 'info/account/logout.html')
    else:
        return redirect('login')

def register(request):
    if not request.user.is_authenticated:
        return render(request, 'info/account/register.html')
    else:
        return redirect('home')

def handler404(request, exception=None):
    return HttpResponseRedirect('/')

def handler500(request, exception=None):
    return HttpResponseRedirect('/')