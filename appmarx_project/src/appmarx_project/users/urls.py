from django.conf.urls.defaults import *

urlpatterns = patterns('appmarx_project.users.views',
    (r'^login/$', 'login'),
    (r'^signup/$', 'signup'),
    (r'^activate/(?P<activation_code>[a-zA-Z0-9]{32})/$', 'activate')
)
