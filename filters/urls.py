from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.upload_file, name='main_app'),
    url(r'^keywords/$', views.filter_keywords_list, name='keywords'),
    url(r'^contact$', views.contact_form), # delete later
]