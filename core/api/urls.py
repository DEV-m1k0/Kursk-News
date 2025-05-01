from django.urls import path,include
from .views import *

urlpatterns = [
    path('approvedposts/', ApprovedPostsView.as_view()),
    path('banner/', BannerView.as_view()),
    path('postbycategory/',PostsByCategoryView.as_view()),
    path('postsonreview/',OnReviewPostsView.as_view()),
    path('post/<int:id>/', PostInfoView.as_view()),
    path('users/', PostInfoView.as_view())
]