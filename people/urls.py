from django.conf.urls import url

from people.views import CreatorsListView, StaffListView

urlpatterns = [
    url(r'^creators/$', CreatorsListView.as_view(), name='creators-list'),
    url(r'^staff/$', StaffListView.as_view(), name='staff-list'),
]
