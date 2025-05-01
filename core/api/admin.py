from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['email', 'username', 'is_staff', 'is_active', 'is_superuser']
    list_filter = ['is_staff', 'is_superuser', 'is_active']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('username','role')}),
        ('Permissions', {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_superuser')}
        ),
    )
    search_fields = ('email', 'username')
    ordering = ('email',)
    
# Добавление моделей в админ панель
admin.site.register(Post)
admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Like)
admin.site.register(Comment)
admin.site.register(Banner)
admin.site.register(Subscription)
