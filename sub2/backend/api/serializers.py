from accounts.models import Profile
from .models import *
from rest_framework import serializers


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = '__all__'


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = '__all__'

class StoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "store_name",
        ]

# 이렇게 해야 되는 건데 왜...
class ReviewUserSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    class Meta:
        model = Review
        # fidels = ("reviewId","userId","storeId","contents")
        fields = '__all__'

# # add juheekim
# class StoreRecoSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Store
#         fields = '__all__'