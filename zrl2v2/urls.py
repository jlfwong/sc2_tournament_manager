from django.conf.urls.defaults import *
from django.views.static import *
from django.views.generic.simple import direct_to_template
from views import data_handle
from views import auth

urlpatterns = patterns('',
    # 2v2
    (r'^$', direct_to_template, {'template': '2v2/index.html'}),
    (r'^auth', auth),
    (r'^data.json$', data_handle),
)
