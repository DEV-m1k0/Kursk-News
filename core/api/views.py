from django.shortcuts import render
from rest_framework import generics
from .models import *
from .serializers import *
from rest_framework.response import Response

class PostsView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
class AdView(generics.ListCreateAPIView):
    queryset = AdBanner.objects.all()
    serializer_class = AdSerializer
    
    
    


