from django import forms
from .models import *
from django.contrib.auth.forms import (
    AuthenticationForm,
    PasswordChangeForm,
    PasswordResetForm,
    SetPasswordForm,
    UserCreationForm
)

class MySetPasswordForm(SetPasswordForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['new_password1'].widget.attrs = {
            'class': "form-control"
        }
        self.fields['new_password2'].widget.attrs = {
            'class': "form-control"
        }

class MyPasswordResetForm(PasswordResetForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {
            'class': "form-control"
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'comment-textarea',
                'rows': 5,
                'placeholder': 'Напишите ваш комментарий...'
            })
        }

class EmailAuthenticationForm(AuthenticationForm):
    """
    Форма для входа с помощью почты
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget.attrs = {
            'class': 'form-control'
        }

    username = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={
        'class': 'form-control',
    }))


class CustomUserCreationForm(UserCreationForm):
    """
    Кастомная форма для создания аккаунта
    """
    class Meta:
        model = CustomUser
        fields = ('email', 'username', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['email'].widget.attrs = {
            'class': "form-control"
        }
        self.fields['username'].widget.attrs = {
            'class': "form-control"
        }
        self.fields['password1'].widget.attrs = {
            'class': "form-control"
        }
        self.fields['password2'].widget.attrs = {
            'class': "form-control"
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email