from django.contrib import admin
from .models import *

# Добавление моделей в админ панель
admin.site.register(Post)
admin.site.register(CustomUser)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Banner)
