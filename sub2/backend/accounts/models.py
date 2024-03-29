from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # user = models.OneToOneField(User, on_delete=models.CASCADE)
    # gender = models.CharField(max_length=5, null=True, blank=True)
    # age = models.IntegerField()

    id = models.AutoField(primary_key=True)
    nickname = models.CharField(max_length=5, null=True, blank=True)
    gender = models.CharField(max_length=5, null=True, blank=True)
    age = models.IntegerField(default=0)


# 토큰추가
# from django.conf import settings
# from django.contrib.auth import get_user_model
# from django.db.models.signals import post_save
# from django.dispatch import receiver
# from rest_framework.authtokenmodels import Token

# @receiver(post_save, sender=settings.AUTH_USER_MODEL)
# def create_auth_token(sender, instance=None, created=False, **kwargs):
#     if created:
#         Token.objects.create(user=instance)