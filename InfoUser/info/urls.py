from django.urls import re_path
from info.views import *

urlpatterns = [
    re_path(r'^$', user_profile, name='home'),
    re_path(r'^registration/$', register, name='register'),
    re_path(r'^logout/$', UserLogoutView.as_view(), name='logout'),
    re_path(r'^login/$', UserLoginView.as_view(), name='login'),
]