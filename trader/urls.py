from . import views
from django.conf.urls import url

urlpatterns = [
    url(r'^$', views.main),
    url('trader',views.main),
    url('update_server', views.update_server),
    url('varian', views.varian_view)
]
