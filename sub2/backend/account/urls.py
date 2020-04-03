from django.contrib import admin
from django.urls import path, include
from . import views

# fmt: off
urlpatterns = [
    path("signup/", views.signup, name="signup"),
    path("login/", views.login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("home/", views.home, name="home"),
    path("success/", views.success, name="success"),
    path("joinsuccess/", views.joinsuccess, name="joinsuccess")
]
# fmt: on
