from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.views.generic.base import ContextMixin
import requests
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from datetime import  timedelta
from api.models import *
from django.db.models import Count, Q
from api.views import *
from django.views.generic import CreateView, TemplateView, DetailView, UpdateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from api.forms import CustomUserCreationForm, EmailAuthenticationForm, CommentForm, PostForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages
from .forms import CustomUserForm


class ProfileEditView(UpdateView):
    model = CustomUser
    template_name = 'profile_edit.html'
    context_object_name = 'userinfo'
    form_class = CustomUserForm
    
    def get_success_url(self):
        return f'/profile/{self.get_object().username}'


class MainPageView(generic.TemplateView):
    """
    Представление главной страницы сайта
    """
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получение новостей через API
        try:
            context['news'] = requests.get('http://127.0.0.1:8000/api/v1/posts/').json()
        except:
            context['news'] = None
        
        # Получение рекламы через API
        context['banners'] = requests.get('http://127.0.0.1:8000/api/v1/banner/').json()
        # context['ads'] = AdBanner.objects.all()
        
        # Рассчитываем дату "неделю назад"
        week_ago = timezone.now() - timedelta(days=7)
        
        # Фильтруем новости за последнюю неделю и сортируем от новых к старым
        posts_filtered_by_date = Post.objects.filter(created_at__gte=week_ago, status= 'Утверждена').order_by('-created_at')
        context['posts_filtered_by_date'] = posts_filtered_by_date
        
        # Аннотируем количество лайков за неделю и сортируем
        posts_filtered_by_likes = Post.objects.annotate(
            num_likes=Count(
                'likes',
                filter=Q(likes__created_at__gte=week_ago) # Фильтр лайков за неделю
            )
        ).order_by('-num_likes', '-created_at')
        # Сортировка по лайкам и дате
        context['posts_filtered_by_likes'] = posts_filtered_by_likes
        if len(posts_filtered_by_likes) > 1:
            context['last_five_posts_filtered_by_likes'] = posts_filtered_by_likes[1:5]
        
        # Получение самой популярной новости по лайка. Если такой нет, то возвращаяет None
        try:
            most_popular_post = posts_filtered_by_likes.first() if posts_filtered_by_likes.first().num_likes >0 else None
        except:
            most_popular_post = None
        context['most_popular_post'] = most_popular_post
        return context

class CustomLoginView(LoginView):
    """
    Представление страницы входа на сайте
    """
    form_class = EmailAuthenticationForm
    template_name = 'login.html'

class SignUpView(CreateView):
    """
    Представление страницы регистрации аккаунта на сайте
    """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
    

class CategoryView(TemplateView, ContextMixin):
    """
    Представление страницы со всеми новостями и категориями
    """
    template_name = 'category.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение новостей через API
        try:
            context['posts'] = requests.get('http://127.0.0.1:8000/api/v1/approvedposts/').json()
        except:
            context['posts'] = None
        context['categories'] = ['Спорт','Политика']
        return context
    
    def get(self, request = None, *args, **kwargs):
        context = self.get_context_data()
        news = []

        page = request.GET.get('page', 1)

        if 'category' in request.GET:
            cat = request.GET['category']
            if cat == 'all':
                all_news = Post.objects.all()
            else:
                all_news = Post.objects.filter(type=cat)
        else:
            all_news = Post.objects.all().order_by('-created_at')

        paginator = Paginator(all_news, 4)
        
        try:
            news = paginator.page(page)
        except PageNotAnInteger:
            news = paginator.page(1)
        except EmptyPage:
            news = paginator.page(paginator.num_pages)

        context['news'] = news

        return render(request, self.template_name, context)

class PostByIdView(TemplateView):
    """
    Представление новости по id
    """
    template_name = 'details.html'
    
    def get_context_data(self,**kwargs):
        context = super().get_context_data(**kwargs)
        post_id = kwargs['id']
        
        # Получение данных о посте
        post_response = requests.get(f"http://127.0.0.1:8000/api/v1/post/{post_id}/")
        context['postinfo'] = post_response.json()
        
        # Комментарии и форма
        context['comments'] = Comment.objects.filter(post_id=post_id).order_by('-created_at')
        context['comment_form'] = CommentForm()
        
        # Информация о лайках
        context['likes_count'] = Like.objects.filter(post_id=post_id).count()
        context['has_liked'] = False
        if self.request.user.is_authenticated:
            context['has_liked'] = Like.objects.filter(
                post_id=post_id, 
                user=self.request.user
            ).exists()
            
        return context
    
    def post(self, request, *args, **kwargs):
        post_id = kwargs['id']
        post = Post.objects.get(id=post_id)
        
        # Обработка комментариев
        if 'add_comment' in request.POST:
            form = CommentForm(request.POST)
            if form.is_valid() and request.user.is_authenticated:
                Comment.objects.create(
                    post=post,
                    user=request.user,
                    text=form.cleaned_data['text']
                )
        
        # Обработка лайков
        elif 'toggle_like' in request.POST and request.user.is_authenticated:
            like, created = Like.objects.get_or_create(
                post=post,
                user=request.user
            )
            if not created:
                like.delete()
        
        return redirect('postdetail', id=post_id)
    
class ProfileView(TemplateView, LoginRequiredMixin):
    """
    Представление профиля пользователя
    """
    template_name = 'profile.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        username = kwargs['username']
        user = get_object_or_404(CustomUser, username=username)
        user_posts = Post.objects.filter(author=user)
        is_subscribed = False
    
        if self.request.user.is_authenticated:
            is_subscribed = Subscription.objects.filter(
                user=self.request.user, 
                author=user
            ).exists()
        context['userinfo'] = user
        context['is_subscribed'] = is_subscribed
        context['userposts'] = user_posts
        return context
    
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

class SubscribeView(TemplateView):
    """
    Обработчик подписки/отписки на пользователя
    """
    template_name = 'profile.html'
    
    def post(self, request, username):
        author = get_object_or_404(CustomUser, username=username)

        if request.user == author:
            return HttpResponseForbidden("Нельзя подписаться на самого себя!")
        
        subscription, created = Subscription.objects.get_or_create(
            user=request.user,
            author=author
        )
        
        if not created:
            subscription.delete()
            messages.success(request, "Вы успешно отписались!")
        else:
            messages.success(request, "Вы успешно подписались!")
        return redirect('profile', username=username)

class PostCreateView(LoginRequiredMixin, CreateView):
    """
    Представление создания новости
    """
    model = Post
    form_class = PostForm
    template_name = 'create_post.html'
    success_url = '/'

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    
class AllUsersView(TemplateView, ContextMixin):
    """
    Представление страницы со всеми пользователями 
    """
    template_name = 'all_users.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение пользователей через API
        context['users'] = requests.get('http://127.0.0.1:8000/api/v1/users/').json()
        return context

class OnReviewPostsView(TemplateView, ContextMixin):
    """
    Представление страницы с новостями на рассмотрении
    """
    template_name = 'on_review.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение пользователей через API
        context['posts'] = requests.get('http://127.0.0.1:8000/api/v1/postsonreview/').json()
        return context