from django.urls import path
from calculator.views import new_loan, new_payment, get_balance

urlpatterns = [
    path('new_loan/', new_loan, name="new_loan"),
    path('new_payment/', new_payment, name="new_payment"),
    path('get_balance/', get_balance, name="get_balance")
]