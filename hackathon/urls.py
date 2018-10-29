from django.urls import path
from django.conf.urls import include,url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('hold/', views.holdHackathon, name='holdHackathon'),
    path('list/', views.listHackathon, name='listHackathon'),
    url(r'^admin/(?P<HackathonInformation_id>\d+)/$', views.adminHackathon),
    url(r'^admin/(?P<HackathonInformation_id>\d+)/(?P<Team_id>\d+)/$', views.adminHackathon),
    url(r'^list/(?P<HackathonInformation_id>\d+)/$', views.applyHackathon),
    url(r'^page/main/(?P<HackathonInformation_id>\d+)/$', views.mainpageHackathon, name='mainpageHackathon'),
    url(r'^page/teamlist/(?P<HackathonInformation_id>\d+)/$', views.teamlistHackathon),
    url(r'^page/teamlist/(?P<HackathonInformation_id>\d+)/(?P<Team_id>\d+)/$', views.applyTeam)
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
