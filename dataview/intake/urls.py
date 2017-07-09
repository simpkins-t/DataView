from django.conf.urls import url

from intake import views

urlpatterns = [
    url(r'^$', views.site_list, name='site-list'),
    url(r'^sites/(?P<site_id>[0-9]+)/', views.site_detail, name='site-detail'),
    url(r'^sensors/(?P<sensor_id>[0-9]+)/', views.sensor_detail, name="sensor-detail"),
    url(r'^login/', views.login_form, name="login"),
    url(r'^authenticate/', views.auth, name="authenticate")
]