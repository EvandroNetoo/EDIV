from django import forms as django_forms
from django.core.exceptions import ValidationError
from django.contrib.auth import forms, authenticate, login

from typing import Any

from .models import User

class UserChangeForm(forms.UserChangeForm):
    class Meta(forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(forms.UserCreationForm):
    class Meta(forms.UserCreationForm.Meta):
        model = User

class RegisterForm(UserCreationForm):
    '''Form for register users without admin permissions'''
    
    class Meta(UserCreationForm.Meta):
        fields = ('username', 'email', 'first_name')

        
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        
        for fild in self.fields:
            if self.fields[fild] is not None:
                self.fields[fild].help_text = None
            self.fields[fild].widget.attrs.update({'class': 'form-control'})
            
    
class AuthForm(django_forms.Form):
    username_email = django_forms.CharField(
        max_length = 254,
        label = 'Usuário ou email',
        widget = django_forms.TextInput(attrs={'class': 'form-control'}),
    )
    password = django_forms.CharField(
        label = 'Senha',
        strip = False,
        widget = django_forms.TextInput(attrs={'class': 'form-control'}),
    )
    
    error_messages = {
        'invalid_login': 'Usuário/email e/ou senha iválidos.',
        'inactive': 'Usuário foi ativado.',
    }
    
    def clean(self):
        username_email = self.cleaned_data['username_email']
        password = self.cleaned_data['password']
        
        self.user = authenticate(username=username_email, password=password)
        if not self.user:
            raise self.get_invalid_login_error()
        else:
            self.comfirm_user_active()
            
        return self.cleaned_data
    
    def log_into(self, request):
        if not self.user:
            raise TypeError('self.user cant be None, execute form.is_valid() first.')
        
        login(request, self.user)
        return self.user
        
    def get_invalid_login_error(self) -> ValidationError:
        return ValidationError(
            self.error_messages['invalid_login'],
            code='invalid_login'
        )
        
    def comfirm_user_active(self):
        if not self.user.is_active:
            raise ValidationError(
            self.error_messages['inactive'],
            code='inactive'
        )

