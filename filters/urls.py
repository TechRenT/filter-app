from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.upload_file, name='main_app'),
    url(r'^keywords/$', views.filter_keywords_list, name='keywords'),
    url(r'^keyword_create/$', views.keyword_create, name='keyword_create'),
    url(r'^(?P<keyword_pk>\d+)/keyword_create/$', views.keyword_edit, name='keyword_edit'),
    url(r'^(?P<keyword_pk>\d+)/keyword_delete/$', views.keyword_delete, name='keyword_delete'),
    url(r'^url_to_domain/$', views.url_to_domain, name='url_to_domain'),
]