from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Account, Income, Expense, Budget
from datetime import datetime
from django.db.models import Q
from .forms import IncomeForm, ExpenseForm
from django.http import JsonResponse
import requests



@login_required
def dashboard(request):
  # Pass through relevent data 
  accounts = Account.objects.filter(user=request.user)
  balance = 0
  for account in accounts: 
    balance += int(account.balance)
  budget = Budget.objects.filter(user=request.user).first()

  filtered_incomes = Income.objects.filter(account__in=accounts)
  incomes = [income.amount for income in filtered_incomes]
  total_incomes = sum(incomes)

  filtered_expenses = Expense.objects.filter(account__in=accounts)
  expenses = [expense.amount for expense in filtered_expenses]
  total_expenses = sum(expenses)

  return render(request, 'dashboard.html', {
    'accounts': accounts, 'balance': balance,
    'budget': budget, 'total_incomes': total_incomes,
    'total_expenses': total_expenses
  })


@login_required
def accounts(request):
  # Pass through relevent data 
  accounts = Account.objects.filter(user=request.user)
  return render(request, 'accounts/accounts.html', {
    'accounts': accounts
  })


@login_required
def account_detail(request, account_id):
  account = Account.objects.get(id=account_id)

  incomes = Income.objects.filter(account=account)
  expenses = Expense.objects.filter(account=account)

  incomes_list = [income.amount for income in incomes]
  total_incomes = sum(incomes_list)

  expenses_list = [expense.amount for expense in expenses]
  total_expenses = sum(expenses_list)


  return render(request, 'accounts/detail.html', {
    'account': account, 'total_incomes': total_incomes,
    'total_expenses': total_expenses, 'incomes': incomes,
    'expenses': expenses
  })


@login_required
def budget(request):
  accounts = Account.objects.filter(user=request.user)

  current_month = datetime.now().month
  current_year = datetime.now().year

  expenses = Expense.objects.filter(
    Q(account__in=accounts),
    date__month=current_month,
    date__year=current_year
    )
  
  expenses_list = [expense.amount for expense in expenses]
  monthly_expenses_sum = sum(expenses_list)

  budget = Budget.objects.filter(user=request.user).first()

  return render(request, 'budget.html', {
    'budget': budget, 'monthly_expenses_sum': monthly_expenses_sum, 'expenses': expenses
  })


@login_required
def stocks(request):
 
  stock_selection = [
  ['Apple', 'AAPL'], ['Amazon', 'AMZN'], ['Microsoft', 'MSFT'], ['Alphabet (Google)', 'GOOGL'], ['Facebook', 'FB'],
  ['Tesla', 'TSLA'], ['Netflix', 'NFLX'], ['Alibaba', 'BABA'], ['JPMorgan Chase', 'JPM'], ['Visa', 'V'],
  ['Johnson & Johnson', 'JNJ'], ['Walmart', 'WMT'], ['Procter & Gamble', 'PG'], ['Mastercard', 'MA'], ['Bank of America', 'BAC'],
  ['Verizon', 'VZ'], ['NVIDIA', 'NVDA'], ['Disney', 'DIS'], ['Adobe', 'ADBE'], ['Coca-Cola', 'KO'], ['Intel', 'INTC'],
  ['PayPal', 'PYPL'], ['Pfizer', 'PFE'], ['Cisco', 'CSCO'], ['Netflix', 'NFLX'], ['Oracle', 'ORCL'], ['Abbott Laboratories', 'ABT'],
  ['Salesforce', 'CRM'], ['Qualcomm', 'QCOM'], ['Home Depot', 'HD'],
  ]

  return render(request, 'stocks.html', {
   'stock_selection': stock_selection
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
  budget = Budget.objects.filter(user=request.user).first()
  expenses = Expense.objects.filter(account__in=accounts)
  incomes = Income.objects.filter(account__in=accounts)



  incomes_list = [income.amount for income in incomes]
  total_incomes = sum(incomes_list)

  expenses_list = [expense.amount for expense in expenses]
  total_expenses = sum(expenses_list)

  balance = total_incomes - total_expenses

  return render(request, 'transactions/transactions.html', {
    'incomes': incomes, 'expenses': expenses, 'accounts': accounts,
    'budget': budget, 'total_incomes': total_incomes,
    'total_expenses': total_expenses, 'balance': balance
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
  success_url = '/accounts/accounts'


class IncomeCreate(LoginRequiredMixin, CreateView):
  model = Income
  form_class = IncomeForm

  def get_form_kwargs(self):
    kwargs = super(IncomeCreate, self).get_form_kwargs()
    kwargs['user'] = self.request.user 
    return kwargs

  def form_valid(self, form):
    response = super().form_valid(form)
    account = form.cleaned_data['account']
    Account.objects.get(id=account.id).update_balance()
    return response


class IncomeUpdate(LoginRequiredMixin, UpdateView):
  model = Income
  form_class = IncomeForm

  def get_form_kwargs(self):
    kwargs = super(IncomeUpdate, self).get_form_kwargs()
    kwargs['user'] = self.request.user 
    return kwargs

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
  form_class = ExpenseForm

  def get_form_kwargs(self):
    kwargs = super(ExpenseCreate, self).get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

  def form_valid(self, form):
    response = super().form_valid(form)
    account = form.cleaned_data['account']
    Account.objects.get(id=account.id).update_balance()
    return response

class ExpenseUpdate(LoginRequiredMixin, UpdateView):
  model = Expense
  form_class = ExpenseForm

  def get_form_kwargs(self):
    kwargs = super(ExpenseUpdate, self).get_form_kwargs()
    kwargs['user'] = self.request.user
    return kwargs

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
  fields = ['amount']

  def form_valid(self, form):
    form.instance.user = self.request.user
    return super().form_valid(form)
  
class BudgetUpdate(LoginRequiredMixin, UpdateView):
  model = Budget
  fields = ['amount']

class BudgetDelete(LoginRequiredMixin, DeleteView):
  model = Budget
  success_url = '/budget'