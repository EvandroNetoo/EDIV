from django.contrib import messages
from django.contrib.messages import constants
from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model, login as login_auth, logout as logout_auth

from .decorators import not_authenticated
from .forms import RegisterForm, AuthForm


def register(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})
    
    elif request.method == 'POST':
        register_form = RegisterForm(request.POST)
        
        if register_form.is_valid():
            form_new = register_form.save(commit=False)
            form_new.is_active = False
            form_new.save()
            return redirect('login')
        return render(request, 'register.html', {'register_form': register_form})


@not_authenticated
def login(request: HttpRequest) -> HttpResponse:
    if request.method == 'GET':
        auth_form = AuthForm()
        return render(request, 'login.html', {'auth_form': auth_form})
    elif request.method == 'POST':
        auth_form = AuthForm(request.POST)
        if auth_form.is_valid():
            if auth_form.log_into(request):
                return redirect('/') # TODO: REDIRECIONAR PARA HOME
        return render(request, 'login.html', {'auth_form': auth_form})

def active_account(request: HttpRequest, uidb4: str, token: str) -> HttpResponse:
    User = get_user_model()
    uid = urlsafe_base64_decode(uidb4)
    user = User.objects.filter(pk=uid)
    if (user := user.first()) and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        login_auth(request, user)
        messages.add_message(request, constants.SUCCESS, 'Usuário ativo com sucesso.')
        return redirect('login')
    else:
        messages.add_message(request, constants.ERROR, 'A url acessada não é valida.')
        return redirect('login') 


def logout(request: HttpRequest) -> HttpResponse:
    logout_auth(request)
    messages.add_message(request, constants.SUCCESS, 'Você foi deslogado com sucesso')
    return redirect('login')
