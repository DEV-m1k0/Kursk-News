# signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Post
from .tasks import notify_subscribers

@receiver(post_save, sender=Post)
def post_created(sender, instance, created, **kwargs):
    if created:
        notify_subscribers(instance.id)  # Запуск фоновой задачи