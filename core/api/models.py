from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    """
    Модель Пользователей
    """
    ROLES = (
        ('user', 'Пользователь'),
        ('copywriter', 'Копирайтер'),
        ('admin', 'Администратор'),
        ('redactor', 'Редактор'),
    )
    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Роль')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class Post(models.Model):
    """
    Модель Новостей
    """
    NEWS_STATUS = (
        ('under_consideration', 'На рассмотрении'),
        ('approver', 'Утверждена'),
        ('rejected', 'Отклонена')
    )
    NEWS_TYPE = (
        ('sport', 'Спорт'),
        ('politics', 'Политика'),
    )
    type = models.CharField(max_length=40, choices=NEWS_TYPE, verbose_name='Тип новости')
    image = models.ImageField(verbose_name='Каптинка новости', upload_to='news_images')
    video = models.TextField(verbose_name='Видеоплеер', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое новости')
    status = models.CharField(max_length=30, choices=NEWS_STATUS, verbose_name='Статус новости')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'

class Comment(models.Model):
    """
    Модель Комментариев
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Новость')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Содержимое комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return f'Комментарий {self.user} под {self.post}'
    
    class Meta:
        verbose_name = 'Комментрий'
        verbose_name_plural = 'Комментарии'
    
class Like(models.Model):
    """
    Модель Лайков
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='Новость')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания', db_index=True)

    def __str__(self):
        return f'Лайк {self.user} для {self.post}'
    
    class Meta:
        unique_together = ('post', 'user')  # Один лайк от пользователя на пост
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'

class AdBanner(models.Model):
    """
    Модель Лайков
    """
    title = models.CharField(max_length=200, verbose_name='Название рекламы')
    image = models.ImageField(verbose_name='Каптинка новости', upload_to='ad_banner')

    def __str__(self):
        return f'Реклама {self.title}'
    
    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Реклама'