from typing import Any
from django import forms
from django.contrib.auth import forms
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
        

