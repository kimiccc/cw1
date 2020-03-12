"""cw1 URL Configuration

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
from django.contrib import admin
from django.urls import path
from app01 import views

urlpatterns = [
    path('/', views.index),
    path('admin/', admin.site.urls),
    path(r'login/', views.login),
    path(r'logout/', views.logout),
    path(r'index/', views.index),
    path(r'register/', views.register),
    path(r'list/', views.list),
    path(r'average/', views.average),
    path(r'rate/', views.rate),
    path(r'view/', views.view),
]