from django.urls import path

from . import views

urlpatterns = [
    # ex: /home /
    path('', views.index, name='index'),
    path('ilanlar',views.properties, name='ilanlar'),
    path('iletisim',views.iletisim, name='iletisim'),
    path('evdetay',views.singleSayfa, name='ev'),

]
