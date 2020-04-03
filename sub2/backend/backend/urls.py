from django.contrib import admin
from django.urls import path, include
import account.views

from django.conf import settings
from django.conf.urls.static import static

# fmt: off
urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/", include("api.urls")),
    path("account/", include("account.urls")),
    path("", account.views.home, name="home")
]
# fmt: on
