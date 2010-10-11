from appmarx_project.users.models import User, User_Activation, User_Website
from django.contrib import admin

admin.site.register(User)
admin.site.register(User_Activation)
admin.site.register(User_Website)