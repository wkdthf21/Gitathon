from django.urls import path
from django.conf.urls import include,url
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('hold/', views.holdHackathon, name='holdHackathon'),
    path('list/', views.listHackathon, name='listHackathon'),
    url(r'^list/(?P<hackathonInformation_id>\d+)/$', views.applyHackathon),
    url(r'^page/main/(?P<hackathonInformation_id>\d+)/$', views.mainpageHackathon),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root = settings.STATIC_ROOT)
