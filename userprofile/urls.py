# coding: utf8
from django.conf.urls import patterns, include, url
from models import *
from userprofile import views
from views import *

# Myghtyboard URLs
urlpatterns = patterns('userprofile',
                       (r'^$', 'views.index'),
                       (r'^avatar/$', 'views.avatar'),)
