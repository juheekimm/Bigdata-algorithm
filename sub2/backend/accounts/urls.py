from django.conf.urls import url, include
from rest_framework.routers import DefaultRouter
from accounts import views, serializers
from django.urls import path


# router = DefaultRouter(trailing_slash=False)
# router.register(r"stores", views.StoreViewSet, basename="stores")

# urlpatterns = router.urls

urlpatterns = [
    url('registration/',include('rest_auth.registration.urls'), name="signup"),
    url('regi/', serializers.CustomRegistrationView.as_view(), name="rest_name_register"),
    url('login/', serializers.CustomLoginView.as_view(), name="CustomLoginView")
]
# from django.contrib import admin
# from django.contrib.auth import views as auth_views
# from django.urls import path, include
# from rest_framework.authtoken import views
# from . import views

# fmt: off
# urlpatterns = [
    # path('posts/', views.posts, name='posts'),
    # path('api-token-auth/', views.obtain_auth_token)
    # path("signup/", views.signup, name="signup"),
    # path("login/", views.login, name="login"),
    # path("logout/", views.logout, name="logout"),
    # path("home/", views.home, name="home"),
    # path("success/", views.success, name="success"),
    # path("joinsuccess/", views.joinsuccess, name="joinsuccess")
    # path('login/', auth_views.LoginView.as_view(), name="login"),
    # path('logout/', auth_views.LogoutView.as_view(), name="logout"),
# ]
# fmt: on
