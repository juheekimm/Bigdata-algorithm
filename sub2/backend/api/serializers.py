from .models import *
from rest_framework import serializers


class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "id",
            "store_name",
            "branch",
            "area",
            "tel",
            "address",
            "latitude",
            "longitude",
            "category_list",
        ]


class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = Menu
        fields = [
            "id",  # 리뷰 고유번호
            "store",  # 음식점 고유번호
            "menu_name",  # 메뉴 이름
            "price",  # 메뉴가격
        ]


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",  # 유저 고유번호
            "gender",  # 성별
            "age",  # 연령
        ]


class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = [
            "id",  # 메뉴 고유번호
            "store",  # 음식점 고유번호
            "user",  # 유저 고유번호
            "score",  # 평점
            "content",  # 리뷰 내용
            "reg_time",  # 리뷰 등록 시간
        ]

class StoreNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = [
            "store_name",
        ]