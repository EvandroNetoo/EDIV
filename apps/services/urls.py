from django.urls import path
from .views import *

urlpatterns = [
    # /services/request_budget
    path('request_budget/', request_budget, name='request_budget'),
]
