from django.shortcuts import render
from django.views import generic
from django.views.generic.base import ContextMixin
import requests
from django.utils import timezone
from datetime import  timedelta
from api.models import *
from django.db.models import Count, Q
from api.views import *
from django.views.generic import CreateView, TemplateView
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from api.forms import CustomUserCreationForm, EmailAuthenticationForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

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
        posts_filtered_by_date = Post.objects.filter(created_at__gte=week_ago).order_by('-created_at')
        context['posts_filtered_by_date'] = posts_filtered_by_date
        
        # Аннотируем количество лайков за неделю и сортируем
        posts_filtered_by_likes = Post.objects.annotate(
            num_likes=Count(
                'likes',
                filter=Q(likes__created_at__gte=week_ago) # Фильтр лайков за неделю
            )
        ).order_by('-num_likes', '-created_at')  # Сортировка по лайкам и дате
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
    template_name = 'category.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Получение новостей через API
        try:
            context['posts'] = requests.get('http://127.0.0.1:8000/api/v1/posts/').json()
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