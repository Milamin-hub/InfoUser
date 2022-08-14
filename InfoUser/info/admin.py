from django.contrib import admin
from info.models import *

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'name', 'username', 'state_id']
admin.site.register(Profile, ProfileAdmin)