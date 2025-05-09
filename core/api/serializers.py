from rest_framework import serializers
from .models import *

class UsernameSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ("username", )

class PostSerializer(serializers.ModelSerializer):
    author = UsernameSerializer()
    class Meta:
        model = Post
        fields = "__all__"

class AdSerializer(serializers.ModelSerializer): 
    class Meta:
        model = Banner
        fields = "__all__"

class CustomUserSerializer(serializers.ModelSerializer): 
    class Meta:
        model = CustomUser
        fields = "__all__"
        

        