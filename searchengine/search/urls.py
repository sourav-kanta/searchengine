from django.conf.urls import url
from . import views

urlpatterns = [
url(r'^crawler$', views.start, name='start'),
	url(r'^search_heavy$', views.search_page, name='crawl_page'),
	 url(r'^$', views.start, name='start'),
		]

