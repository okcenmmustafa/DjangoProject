from django.urls import path

from . import views

urlpatterns = [
    # ex: /home /
    path('', views.index, name='index'),
    path('ilanlar',views.ilanlar, name='ilanlar'),
    path('iletisim',views.iletisim, name='iletisim'),


]
