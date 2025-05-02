from django import forms
from api.models import CustomUser


class CustomUserForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['first_name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['last_name'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['email'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['username'].widget.attrs = {
            'class': 'form-control'
        }
        self.fields['role'].widget.attrs = {
            'class': 'w-100'
        }

    class Meta:
        model = CustomUser
        fields = ["first_name", 'last_name', 'email', 'username', 'role']