from django.conf.urls import patterns, include, url
from books import views


from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'books_pro.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    #url(r'^test$', views.test, name='test'),
    url(r'^$', views.index, name='index'),
    url(r'^login/$', views.login, name='login'),
    url(r'^home/$', views.home, name='home'),
    url(r'^register/$', views.register, name='register'),
    url(r'^admin/', include(admin.site.urls)),
)
