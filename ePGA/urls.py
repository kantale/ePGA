
from django.conf.urls import patterns, url

from ePGA import views

# get_var = r'[\w\ \,]+'
get_var = r'[\w\*\&\(\)\:\>\-\_\ \#\.\,]+'

urlpatterns = patterns('',
    url(r'^$', views.start, name='start'),
    url(r'^about/$', views.about, name='about'),
    url(r'^studies/$', views.studies, name='studies'),
    url(r'^events/$', views.events, name='events'),
    url(r'^explore/$', views.explore, name='explore'),
    url(r'^explore/([\w\*\&\(\)\:\>\-\_\ \#\.]+)/([\w\*\&\(\)\:\>\-\_\ \#\.]+)/$', views.explore_translation, name='explore_translation'),
    url(r'^explore/([\w\*\&\(\)\:\>\-\_\ \#\.]+)/([\w\*\&\(\)\:\>\-\_\ \#\.]+)/fetch_init_json/$', views.fetch_init_json, name='fetch_init_json'),
    url(r'^explore/([\w\*\&\(\)\:\>\-\_\ \#\.]+)/([\w\*\&\(\)\:\>\-\_\ \#\.]+)/recommendations/$', views.recommendations, name='recommendations'),
    url(r'^translate/$', views.translate, name='translate'), 
    url(r'^vote/$', views.test_jquery, name='test_jquery'),
    url(r'^get_genes/$', views.get_genes, name='get_genes'),
    url(r'^get_drugs/$', views.get_drugs, name='get_drugs'),
    url(r'^get_phenotypes/$', views.get_phenotypes, name='get_phenotypes'),
    url(r'^query/$', views.query, name='query'),
    url(r'^explore/recommendations/$', views.recommendations, name='recommendations'),
    url(r'^explore/recommendations/([\w]+)/(%s)$' % get_var, views.recommendations_GET, name='recommendations_GET'),
    url(r'^explore/recommendations/([\w]+)/(%s)/([\w]+)/(%s)$' % (get_var, get_var), views.recommendations_GET, name='recommendations_GET'),
    url(r'^explore/recommendations/([\w]+)/(%s)/([\w]+)/(%s)/([\w]+)/(%s)$' % (get_var, get_var, get_var), views.recommendations_GET, name='recommendations_GET'),
    url(r'^explore/recommendations/([\w]+)/(%s)/([\w]+)/(%s)/([\w]+)/(%s)/([\w]+)/(%s)$' % (get_var, get_var, get_var, get_var) , views.recommendations_GET, name='recommendations_GET'),
    url(r'^rd_connect_api/annotations$', views.rd_connect_GET, name='rd_connect_GET'),
    url(r'^explore/fetch_init_json/$', views.fetch_init_json, name='fetch_init_json'),
    url(r'^upload_file/$', views.upload_file, name='upload_file'),
#    url(r'^index/$', views.index, name='index'),
)

