from django.shortcuts import render
from rest_framework import generics, response
from .models import *
from .serializers import *
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

class ApprovedPostsView(generics.ListCreateAPIView):
    """
    Апи для всех утвержденных новостей
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request):
        obj = Post.objects.filter(status='Утверждена')
        serializer = PostSerializer(obj, many=True)
        return response.Response(serializer.data)

class OnReviewPostsView(generics.ListCreateAPIView):
    """
    Апи для всех утвержденных новостей
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get(self, request):
        obj = Post.objects.filter(status='На рассмотрении')
        serializer = PostSerializer(obj, many=True)
        return response.Response(serializer.data)
    
class BannerView(generics.ListCreateAPIView):
    """
    Апи для рекламы
    """
    queryset = Banner.objects.all()
    serializer_class = AdSerializer

class PostsByCategoryView(generics.ListAPIView):
    """
    Апи для новостей по категории
    """
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
    """
    Апи для новостей по id
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"
    
class UserAPIView(generics.ListAPIView):
    """
    Апи для получения всех постов
    """
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    

