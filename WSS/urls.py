from django.conf.urls import url, include

from WSS.views import HomeView, StaffListView

year_urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^staff/$', StaffListView.as_view(), name='staff-list'),
]

urlpatterns = [
    url(r'^(?P<year>\d{4})/', include(year_urlpatterns)),
    url(r'^$', HomeView.as_view(), name='home'),
]
