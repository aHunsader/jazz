from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index, name='index'),
	url(r'^callSpotify/$', views.callSpotify, name='callSpotify'),
	url(r'^callback/$', views.callback, name='callback'),
]