from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.filter_keywords_list),
]