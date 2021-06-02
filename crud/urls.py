from django.conf.urls import url 
from crud import views 

urlpatterns = [ 
    url(r'^api/crud$', views.crud_list),
    url(r'^api/crud/(?P<pk>[0-9]+)$', views.crud_detail),
    url(r'^api/crud/published$', views.crud_list_published)
]