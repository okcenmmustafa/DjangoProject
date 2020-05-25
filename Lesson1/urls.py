"""Lesson1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from home import views

urlpatterns = [
    path('',include('home.urls')),
    path('admin/' , admin.site.urls) ,
    path('house/',include('house.urls')),
    path('home/',include('home.urls')),
    path('user/',include('user.urls')),
    path('content/',include('content.urls')),
    path('ckeditor/' , include('ckeditor_uploader.urls')) ,
    path('home/' , include('home.urls')) ,


    path('hakkimizda/',views.hakkimizda,name='hakkimizda'),
    path('category/<slug:slug>/<int:id>/',views.category_ilanlar,name='category_ilanlar'),
    path('houses/<slug:slug>/<int:id>/',views.UrunSayfasi,name='UrunSayfasi'),
    path('search/',views.house_search,name='house_search'),
    path('search2/',views.house_search2 ,name='house_search2'),
    path('search_auto/',views.house_search_auto,name='house_search_auto'),


    path('logout/',views.logout_view,name='logout_view'),
    path('login/',views.login_view,name='login_view'),
    path('signup/',views.signup_view,name='signup_view'),
    path('sss/',views.faq,name='faq'),
]
if settings.DEBUG:
    urlpatterns +=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
