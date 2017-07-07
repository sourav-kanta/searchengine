from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^crawler$', views.start, name='start'),
	url(r'^signup$', views.signup, name='signup'),
	url(r'^login/$', 'django.contrib.auth.views.login',kwargs={'template_name': 'crawler/login.html'}, ),
	url(r'^home$', views.home, name='home'),
	url(r'^crawler_heavy$', views.crawl_page, name='crawl_page'),
	url(r'^$', views.signup, name='signup'),
	url(r'^logout/$', views.logout_page,name='logout_page'),

]