from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.upload_file, name='main_app'),
    url(r'^keywords/$', views.filter_keywords_list, name='keywords'),
    url(r'^keyword_create/$', views.keyword_create, name='keyword_create'),
    url(r'^(?P<keyword_pk>\d+)/keyword_edit/$', views.keyword_edit, name='keyword_edit'),
    url(r'^(?P<keyword_pk>\d+)/keyword_delete/$', views.keyword_delete, name='keyword_delete'),
    url(r'^url_to_domain/$', views.url_to_domain, name='url_to_domain'),
    url(r'^qualify_url/$', views.qualify_url, name='qualify_url'),
    url(r'^qualify_url/paper_preservation/$', views.qualify_url_paper_preservation, name='qualify_url_paper_preservation'),
    url(r'^keywords_cbv/$', views.KeywordListView.as_view(), name='keywords_cbv'),
    url(r'^keyword_create_cbv/$', views.KeywordCreateView.as_view(), name='keyword_create_cbv'),
    url(r'^(?P<pk>\d+)/keyword_edit_cbv/$', views.KeywordUpdateView.as_view(), name='keyword_edit_cbv'),
    url(r'^(?P<pk>\d+)/keyword_delete_cbv/$', views.KeywordDeleteView.as_view(), name='keyword_delete_cbv'),
]