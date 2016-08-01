from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^keywords/$', views.filter_keywords_list, name='keywords'),
]