from django.contrib import admin
from .models import User
from django.contrib.auth import admin as admin_auth_django
from .forms import UserChangeForm, UserCreationForm


@admin.register(User)
class UserAdmin(admin_auth_django.UserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm
    model = User
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('username', 'email')
    fieldsets = admin_auth_django.UserAdmin.fieldsets + (   
    )
