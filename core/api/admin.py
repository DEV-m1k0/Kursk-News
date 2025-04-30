from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username',)}),
        ('Permissions', {'fields': ('is_staff',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff')}
        ),
    )
    ordering = ('email',)
    
# Добавление моделей в админ панель
admin.site.register(Post)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Banner)
