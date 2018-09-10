"""profiles_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from profilesapi import views

urlpatterns = [
    url(r'^user/$', views.user),
    url(r'^song/$', views.song),
    url(r'^album/$', views.album),
    url(r'^genre/$', views.genre),
    url(r'^artist/$', views.artist),
    url(r'^playlist/$', views.playlist),
    url(r'^playlist_song/$', views.playlist_song),
    url(r'^rating/$', views.rating),
    url(r'^Recommendation/$', views.Recommendation),
    url(r'^autoget/$', views.autoget)
]
