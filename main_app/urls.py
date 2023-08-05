from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('budget/', views.budget, name='budget'),
    path('settings/', views.settings, name='settings'),
    path('accounts/signup/', views.signup, name='signup'),
    path('transactions/', views.transactions, name='transactions'),
    path('transactions/incomes', views.incomes, name='incomes'),
    path('transactions/expenses', views.expenses, name='expenses'),
    path('demo_account/', views.demo_account, name='demo_account'),
    path('accounts/create/', views.AccountCreate.as_view(), name='account_create'),
    path('accounts/<int:pk>/update/', views.AccountUpdate.as_view(), name='account_update'),
    path('accounts/<int:pk>/delete/', views.AccountDelete.as_view(), name='account_delete'),
]