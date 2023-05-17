from django.urls import path
from .views import *

urlpatterns = [
    # /auth/register/
    path('register/', register, name='register'),
    # /auth/login/
    path('login/', login, name='login'),
    # /auth/active_account/uidb4/token/
    path('active_account/<str:uidb4>/<str:token>/', active_account, name='active_account'),
    # /auth/logout/
    path('logout/', logout, name='logout'),
]
