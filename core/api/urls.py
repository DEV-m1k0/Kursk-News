from django.urls import path,include
from .views import *

urlpatterns = [
    path('posts/', PostsView.as_view()),
    path('banner/', BannerView.as_view()),
    path('postbycategory/',PostsByCategoryView.as_view())
]