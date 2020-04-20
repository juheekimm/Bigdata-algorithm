from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile

class ProfileSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Profile
        fields = ('nickname', 'gender', 'age')


class UserSerializer(serializers.HyperlinkedModelSerializer):
    user = ProfileSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'firstname', 'last name')