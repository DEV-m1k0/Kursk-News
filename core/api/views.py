from django.shortcuts import render
from rest_framework import generics, response
from .models import *
from .serializers import *


class PostsView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class BannerView(generics.ListCreateAPIView):
    queryset = Banner.objects.all()
    serializer_class = AdSerializer

class PostsByCategoryView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request):
        category = request.GET.get('category')
        display_name_to_key = {v: k for k, v in Post.NEWS_TYPE}
        type = display_name_to_key.get(category)
        posts = Post.objects.filter(type=type)
        serializer = PostSerializer(posts, many=True)
        return response.Response(serializer.data)

class PostsByCategoryView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request):
        category = request.GET.get('category')
        display_name_to_key = {v: k for k, v in Post.NEWS_TYPE}
        type = display_name_to_key.get(category)
        posts = Post.objects.filter(type=type)
        serializer = PostSerializer(posts, many=True)
        return response.Response(serializer.data)

class PostInfoView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"
    
    
    


