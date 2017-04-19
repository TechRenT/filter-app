from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.qualify_form, name='qualify_form'),
]