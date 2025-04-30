from django.urls import path,include
from .views import *

urlpatterns = [
    path('posts/', PostsView.as_view()),
    path('ad/', AdView.as_view())
]