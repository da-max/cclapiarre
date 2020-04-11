from django.conf.urls import url

from stats.views import ListPageAccess, CreatePageAccess, UpdatePageAccess

urlpatterns = [
    url(r'^liste-des-acces$', ListPageAccess.as_view(), name='list_pageaccess'),
    url(r'^creer-une-regle-d-acces', CreatePageAccess.as_view(), name='create_pageaccess'),
    url(r'^modifier-une-regle-d-acces/(?P<id_pageaccess>\d+)$', UpdatePageAccess.as_view(), name='update_pageaccess')
]
