from typing import Callable
from django.http import HttpRequest
from django.shortcuts import redirect

def not_authenticated(view_func: Callable, redirect_url: str='/'):
    def _wrapper(request:   HttpRequest, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(redirect_url)
        return view_func(request, *args, **kwargs)
    return _wrapper