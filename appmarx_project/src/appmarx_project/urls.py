from django.conf.urls.defaults import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^appmarx_project/', include('appmarx_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    (r'^admin/', include(admin.site.urls)),
    #(r'^users/login/$', 'appmarx_project.users.views.login'),
    (r'^users/', include('appmarx_project.users.urls')),
    (r'^websites/', include('appmarx_project.websites.urls')),
)
