# coding: utf8
from django.conf.urls import patterns, include, url
from models import *
from books_app import views
from views import *

urlpatterns = patterns('',
    (r'create/$', create_book,),
    (r'^$', list_book),
    (r'^wereview$', wereview),
    (r'^mybooklist$', booklist),
    (r'edit/(?P<id>[^/]+)/$', edit_book),
    (r'view/(?P<id>[^/]+)/$', view_book),
    
)
