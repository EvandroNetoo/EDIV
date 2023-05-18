from django.urls import path
from .views import *

urlpatterns = [
    # /services/request_budget
    path('request_budget/', BudgetRequestView.as_view(), name='request_budget'),
]
