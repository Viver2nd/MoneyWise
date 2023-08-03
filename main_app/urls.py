from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('transactions/', views.transactions, name='transactions'),
    path('budget/', views.budget, name='budget'),
    path('settings/', views.settings, name='settings'),
]