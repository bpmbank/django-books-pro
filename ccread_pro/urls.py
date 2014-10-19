# coding: utf8
from django.conf.urls import patterns, include, url
from django.contrib import admin
from books_app import views


admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^books/', include('books_app.urls')),  # 此处不能加$
    url(r'^userprofile/', include('userprofile.urls')),
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.login, name='login'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^admin/', include(admin.site.urls)),
)
