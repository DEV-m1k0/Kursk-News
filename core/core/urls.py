"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from app.views import *
from django.contrib.auth import views as auth_views
from api.forms import (
    MyPasswordResetForm,
    MySetPasswordForm
)
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include('api.urls')),
    path('', MainPageView.as_view(), name='index'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('category/', CategoryView.as_view(), name='category'),
    path('post/<int:id>/',PostByIdView.as_view(), name='postdetail'),
    path('profile/<str:username>/', ProfileView.as_view(), name='profile'),
    path('subscribe/<str:username>/', SubscribeView.as_view(), name='toggle_subscription'),
    path('create_post/', PostCreateView.as_view(), name='post_create'),
    path('all_users/',AllUsersView.as_view(), name='all_users'),
    path('on_review_posts/', OnReviewPostsView.as_view(), name='on_review_posts'),
    path('on_review_posts/<int:pk>/', PostEditView.as_view(), name='post_edit'),
    path('on_review_posts/<int:pk>/decline/', PostDeclineView.as_view(), name='post_decline'),
    path('on_review_posts/<int:pk>/accept/', PostAcceptView.as_view(), name='post_accept'),
    path('profile/<int:pk>/edit/', ProfileEditView.as_view(), name='profile_edit'),

    # Сьрос пароля через почту
    path('password_reset/', auth_views.PasswordResetView.as_view(
        email_template_name='registration/password_reset_email.html',
        template_name='registration/password_reset_form.html',
        form_class=MyPasswordResetForm
        ), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(form_class=MySetPasswordForm), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
