from django.urls import re_path
from . import views


urlpatterns = [
    re_path('^$', views.show),
    re_path('showOne/(?P<video_id>\d+)/$', views.ShowOneVideo),
    re_path('addcomment/(?P<video_id>\d+)/$', views.addcomment),
    re_path('sign/',views.sign),
    re_path('in/', views.inn),
    re_path('out/', views.out),
    re_path('addliketovideo/(?P<video_id>\d+)/$', views.addliketovideo),
    re_path('addliketocomment/(?P<comment_id>\d+)/$', views.addliketocomment),
    re_path('addliketovideo/ajax/', views.ajax),
    re_path('addliketocomment/ajax1', views.ajax1),
]
