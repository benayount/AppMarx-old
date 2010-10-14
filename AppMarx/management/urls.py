from django.conf.urls.defaults import *

urlpatterns = patterns('management.views',
    (r'^login/$', 'login'),
    (r'^signup/$', 'signup'),
    (r'^logout/$', 'logout'),
    (r'^forget_password/$', 'forget_password'),
    (r'^activate/(?P<activation_code>[a-zA-Z0-9]{32})/$', 'activate'),
    (r'^tryit/$', 'tryit'),
    (r'^recommend/(?P<from_id>\d+)/(?P<to_id>\d+)$', 'recommend'),
    (r'^change_password/(?P<token>[a-zA-Z0-9]{32})/$', 'change_password'),
)
