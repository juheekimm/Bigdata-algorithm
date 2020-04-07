from django.utils import timezone
from django.db import models


class Store(models.Model):
    id = models.IntegerField(primary_key=True)
    store_name = models.CharField(max_length=50)
    branch = models.CharField(max_length=20, null=True)
    area = models.CharField(max_length=50, null=True)
    tel = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=200, null=True)
    latitude = models.FloatField(max_length=10, null=True)
    longitude = models.FloatField(max_length=10, null=True)
    category = models.CharField(max_length=200, null=True)

    @property
    def category_list(self):
        return self.category.split("|") if self.category else []


class Menu(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    menu_name = models.CharField(max_length=50)
    price = models.IntegerField(default=0)

    def __str__(self):
        return [self.id, self.store, self.menu_name]


class User(models.Model):
    id = models.IntegerField(primary_key=True)
    gender = models.CharField(max_length=10)
    age = models.IntegerField(default=0)

    def __str__(self):
        return [self.id, self.gender, self.age]


class Review(models.Model):
    id = models.IntegerField(primary_key=True)
    store = models.ForeignKey(Store,on_delete=models.CASCADE)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    total_score = models.IntegerField(default=0)
    content = models.CharField(max_length=50)
    reg_time = models.DateTimeField(auto_now=True)

    def __str__(self):
        return [self.id, self.store, self.user, self.total_score]
