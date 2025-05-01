# tasks.py
from background_task import background
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .models import Post, Subscription

@background(schedule=0)  # Немедленное выполнение
def notify_subscribers(post_id):
    post = Post.objects.get(id=post_id)
    author = post.author
    subscribers = Subscription.objects.filter(author=author).select_related('user')
    
    for sub in subscribers:
        if sub.user.email:
            send_mail(
                subject=f'Новая запись от {author.username}',
                message=f'{author.username} только что выпустил новый пост! \n\nЧитать полностью: http://127.0.0.1:8000/post/{post.pk}/',
                from_email='kgpk527@gmail.com',
                recipient_list=[sub.user.email],
                fail_silently=False,
            )