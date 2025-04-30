from django.db import models
from django.contrib.auth.models import AbstractUser
from .validators import validate_image_aspect_ratio, validate_ad_image
from PIL import Image
from io import BytesIO
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.core.validators import FileExtensionValidator
from django.utils.translation import gettext_lazy as _

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
    email = models.EmailField(_('email address'), unique=True)
    username = models.CharField(_('username'), max_length=150, unique=True)
    role = models.CharField(max_length=20, choices=ROLES, verbose_name='Роль', default='user')
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
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
    image = models.ImageField(verbose_name='Каптинка новости', upload_to='news_images', validators=[validate_image_aspect_ratio,FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])])
    video = models.TextField(verbose_name='Видеоплеер', blank=True, null=True)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Автор')
    title = models.CharField(max_length=200, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Содержимое новости',)
    status = models.CharField(max_length=30, choices=NEWS_STATUS, verbose_name='Статус новости',default='under_consideration')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if self.image:
            # Открытие и обработка изображения
            img = Image.open(self.image)
            if img.mode in ('RGBA', 'P'):
                img = img.convert('RGB')
            
            # Размер, к которому приводим изображение
            target_size = (1024, 768)
            img = img.resize(target_size, Image.LANCZOS)
            
            # Сохранение в буфер
            output = BytesIO()
            img.save(output, format='JPEG', quality=95)
            output.seek(0)
            
            # Замена исходного файла
            self.image = InMemoryUploadedFile(
                output,
                'ImageField',
                self.image.name,
                'uploads/jpeg',
                output.tell(),
                None
            )
        
        super().save(*args, **kwargs)

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

class Banner(models.Model):
    """
    Модель Рекламы
    """
    title = models.CharField(max_length=200, verbose_name='Название рекламы')
    image = models.ImageField(verbose_name='Каптинка новости', upload_to='ad_banner',validators=[validate_ad_image, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])],help_text="Требования: горизонтальная ориентация, соотношение 1.91:1, минимум 600x314px, размер файла до 5МБ.")

    def __str__(self):
        return f'Реклама {self.title}'
        
    class Meta:
        verbose_name = 'Реклама'
        verbose_name_plural = 'Реклама'