from django import forms
from .models import *
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

class CommentForm(forms.ModelForm):
    """
    Форма для комментариев
    """
    class Meta:
        model = Comment
        fields = ['text']

class EmailAuthenticationForm(AuthenticationForm):
    """
    Форма для входа с помощью почты
    """
    username = forms.EmailField(label='Email')

class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма для создания аккаунта
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email