from django.conf.urls import url
from sync import views

urlpatterns = [
    url(r'^index/$', views.index),
    url(r'^run/$', views.run),

]