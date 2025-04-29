from django.db import models
from django.contrib.auth.models import AbstractUser

# Модель Пользователей
class CustomUser(AbstractUser):
    ROLES = (
        ('user', 'Пользователь'),
        ('reporter', 'Репотртёр'),
        ('admin', 'Администратор'),
        ('redactor', 'Редактор'),
    )
    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Роль')
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

# Модель Новостей
class Post(models.Model):
    """
    
    """
    NEWS_STATUS = (
        ('under_consideration', 'На рассмотрении'),
        ('approver', 'Утверждена'),
        ('rejected', 'Отклонена')
    )
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

# Модель Комментариев
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments', verbose_name='Новость')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Содержимое комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return f'Комментарий {self.user} под {self.post}'
    
    class Meta:
        verbose_name = 'Комментрий'
        verbose_name_plural = 'Комментарии'
    
# Модель Лайков
class Like(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='likes', verbose_name='Новость')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    def __str__(self):
        return f'Лайк {self.user} для {self.post}'
    
    class Meta:
        unique_together = ('post', 'user')  # Один лайк от пользователя на пост
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'