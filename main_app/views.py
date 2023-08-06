from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account, Income, Expense, Budget


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
  accounts = Account.objects.filter(user=request.user)
  return render(request, 'accounts.html', {
    'accounts': accounts
  })


@login_required
def budget(request):
  # Pass through relevent data 

  budgets = Budget.objects.filter(user=request.user)
  return render(request, 'budget.html', {
    'budgets': budgets
  })


@login_required
def calculator(request):
  # Pass through relevent data 

  return render(request, 'calculator.html')


@login_required
def settings(request):
  # Pass through relevent data 

  return render(request, 'settings.html')


@login_required
def transactions(request):
  # Pass through relevent data 

  accounts = Account.objects.filter(user=request.user)
  expenses = Expense.objects.filter(account__in=accounts)
  incomes = Income.objects.filter(account__in=accounts)

  return render(request, 'transactions/transactions.html', {
    'incomes': incomes, 'expenses': expenses, 'accounts': accounts
  })


def incomes(request):
  # Pass through relevent data 

  accounts = Account.objects.filter(user=request.user)

  incomes = Income.objects.filter(account__in=accounts)


  return render(request, 'transactions/incomes.html', {
    'incomes': incomes
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


class AccountCreate(LoginRequiredMixin, CreateView):
  model = Account
  fields = ['name']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
class AccountUpdate(LoginRequiredMixin, UpdateView):
  model = Account
  fields = ['name']

class AccountDelete(LoginRequiredMixin, DeleteView):
  model = Account
  success_url = '/accounts'


class IncomeCreate(LoginRequiredMixin, CreateView):
  model = Income
  fields = ['amount', 'category', 'description', 'account']

  def form_valid(self, form):
    response = super().form_valid(form)
    account = form.cleaned_data['account']
    Account.objects.get(id=account.id).update_balance()
    return response


class IncomeUpdate(LoginRequiredMixin, UpdateView):
  model = Income
  fields = ['amount', 'category', 'description', 'account']

  def form_valid(self, form):
    response = super().form_valid(form)
    account = form.cleaned_data['account']
    Account.objects.get(id=account.id).update_balance()
    return response

class IncomeDelete(LoginRequiredMixin, DeleteView):
  model = Income
  success_url = '/transactions/incomes'

  def form_valid(self, form):
    response = super().form_valid(form)
    accounts = Account.objects.all()
    for acc in accounts: acc.update_balance()
    return response


class ExpenseCreate(LoginRequiredMixin, CreateView):
  model = Expense
  fields = ['amount', 'category', 'description', 'account']

  def form_valid(self, form):
    response = super().form_valid(form)
    account = form.cleaned_data['account']
    Account.objects.get(id=account.id).update_balance()
    return response

class ExpenseUpdate(LoginRequiredMixin, UpdateView):
  model = Expense
  fields = ['amount', 'category', 'description', 'account']

  def form_valid(self, form):
    response = super().form_valid(form)
    account = form.cleaned_data['account']
    Account.objects.get(id=account.id).update_balance()
    return response

class ExpenseDelete(LoginRequiredMixin, DeleteView):
  model = Expense
  success_url = '/transactions/expenses'

  def form_valid(self, form):
    response = super().form_valid(form)
    accounts = Account.objects.all()
    for acc in accounts: acc.update_balance()
    return response
  

class BudgetCreate(LoginRequiredMixin, CreateView):
  model = Budget
  fields = ['date_from', 'date_to', 'amount']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
class BudgetUpdate(LoginRequiredMixin, UpdateView):
  model = Budget
  fields = ['date_from', 'date_to', 'amount']

class BudgetDelete(LoginRequiredMixin, DeleteView):
  model = Budget
  success_url = '/budget'