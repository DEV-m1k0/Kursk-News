from django.shortcuts import render
from django.views import generic
import requests
from django.utils import timezone
from datetime import  timedelta
from api.models import *
from django.db.models import Count, Q

class MainPageView(generic.TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Получение новостей через API
        context['posts'] = requests.get('http://127.0.0.1:8000/api/v1/posts/').json()
        
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

