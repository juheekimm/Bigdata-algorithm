from django.contrib import admin
from api import models

# Register your models here.

admin.site.register(models.Store)
admin.site.register(models.Menu)
# admin.site.register(models.User)
admin.site.register(models.Review)
