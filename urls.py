from django.conf.urls.defaults import *
from django.views.static import *
from django.contrib.auth.views import login, logout
from django.conf import settings
from players.views import sc2ranks
import tournament.views

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # 2v2
    (r'^2v2/', include('zrl2v2.urls')),
    
    (r'^$',tournament.views.home),
    (r'^players$',tournament.views.players),
    (r'^login$',login,{
        'template_name':'login.html'
    }),
    (r'^logout$',logout),

    (r'^admin/players/player/sc2ranks', sc2ranks),

    (r'^admin/', include(admin.site.urls)),
    (r'^site_media/(?P<path>.*)$','django.views.static.serve',{
        'document_root': settings.MEDIA_ROOT
    }),
)
