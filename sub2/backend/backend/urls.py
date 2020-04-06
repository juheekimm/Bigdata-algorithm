from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
# import accounts.views
from accounts.views import profile

# from django.conf import settings
# from django.conf.urls.static import static

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls),
    
    path("api/", include("api.urls")),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('profile/', profile, name='profile'),
    # path("accounts/", include("accounts.urls")),
    # path('accounts/', include('django.contrib.auth.urls')),
    # path('', accounts.views.base, name="base"), 
    # path("", accounts.views.home, name="home").
    # path('admin/', admin.site.urls),
]
# fmt: on
