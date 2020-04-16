from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from . import views
from django.urls import path

urlpatterns = [
    url('index/', views.index, name="index"),
]