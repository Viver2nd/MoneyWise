from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account, Income, Expense


@login_required
def dashboard(request):
  # Pass through relevent data 
  accounts = Account.objects.filter(user=request.user)
  return render(request, 'dashboard.html', {
    'accounts': accounts
  })


@login_required
def accounts(request):
  # Pass through relevent data 

  return render(request, 'accounts.html')


@login_required
def budget(request):
  # Pass through relevent data 

  return render(request, 'budget.html')


@login_required
def settings(request):
  # Pass through relevent data 

  return render(request, 'settings.html')


@login_required
def transactions(request):
  # Pass through relevent data 

  return render(request, 'transactions/transactions.html')


def incomes(request):
  # Pass through relevent data 

  accounts = Account.objects.filter(user=request.user)

  incomes = Income.objects.filter(account__in=accounts)

  return render(request, 'transactions/incomes.html', {
    'accounts': accounts, 'incomes': incomes
  })


def expenses(request):
  # Pass through relevent data 

  accounts = Account.objects.filter(user=request.user)

  expenses = Expense.objects.filter(account__in=accounts)

  return render(request, 'transactions/expenses.html', {
    'accounts': accounts, 'expenses': expenses
  })


def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('dashboard')
    else:
      error_message = 'Invalid, Try Again'
  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message } 
  return render(request, 'registration/signup.html', context)


def demo_account(request):
  # Check if the user is already logged in
  if request.user.is_authenticated:
    return redirect('dashboard')

  # Authenticate the demo account
  user = authenticate(username='admin', password='1234')
  login(request, user)
  return redirect('dashboard')
