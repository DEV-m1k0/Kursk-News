from django.shortcuts import render
from rest_framework import generics, response
from .models import *
from .serializers import *
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.renderers import BrowsableAPIRenderer, JSONRenderer
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie

class ApprovedPostsView(generics.ListCreateAPIView):
    """
    Апи для всех утвержденных новостей
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [JSONParser, MultiPartParser]
    renderer_classes = [JSONRenderer]
    
    @method_decorator(cache_page(60 * 60 * 2))
    @method_decorator(vary_on_cookie)
    def get(self, request):
        obj = Post.objects.filter(status='Утверждена')
        serializer = PostSerializer(obj, many=True)
        return response.Response(serializer.data)

class OnReviewPostsView(generics.ListCreateAPIView):
    """
    Апи для всех утвержденных новостей
    """
    renderer_classes = [JSONRenderer]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    parser_classes = [JSONParser, MultiPartParser]
    
    def get(self, request):
        obj = Post.objects.filter(status='На рассмотрении')
        serializer = PostSerializer(obj, many=True)
        return response.Response(serializer.data)
    
class BannerView(generics.ListCreateAPIView):
    """
    Апи для рекламы
    """
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser, MultiPartParser]
    queryset = Banner.objects.all()
    serializer_class = AdSerializer

class PostsByCategoryView(generics.ListAPIView):
    """
    Апи для новостей по категории
    """
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    parser_classes = [JSONParser, MultiPartParser]
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
    renderer_classes = [JSONRenderer]
    parser_classes = [JSONParser, MultiPartParser]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = "id"
    
class UserAPIView(generics.ListAPIView):
    """
    Апи для получения всех постов
    """
    renderer_classes = [BrowsableAPIRenderer, JSONRenderer]
    parser_classes = [JSONParser, MultiPartParser]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    

