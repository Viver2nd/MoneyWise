from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('transactions/', views.transactions, name='transactions'),
    path('budget/', views.budget, name='budget'),
    path('settings/', views.settings, name='settings'),
    path('accounts/signup/', views.signup, name='signup'),
    path('demo_account/', views.demo_account, name='demo_account'),
]