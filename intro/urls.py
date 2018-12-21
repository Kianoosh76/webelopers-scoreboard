from django.conf.urls import url

from intro.views import HomeView, StaffView

urlpatterns = [
    url(r'^$', HomeView.as_view(), name='home'),
    url(r'^staff/$', StaffView.as_view(), name='staff')
]
