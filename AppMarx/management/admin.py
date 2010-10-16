from models import Website, Website_Website, \
 User, User_Activation, User_Website, User_AutoLogin, Website_Image
 
from django.contrib import admin

admin.site.register(User)
admin.site.register(User_Activation)
admin.site.register(User_Website)
admin.site.register(User_AutoLogin)
admin.site.register(Website)
admin.site.register(Website_Website)
admin.site.register(Website_Image)