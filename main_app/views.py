from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


@login_required
def dashboard(request):
  # Pass through relevent data 
  
  return render(request, 'dashboard.html')


@login_required
def accounts(request):
  # Pass through relevent data 

  return render(request, 'accounts.html')


@login_required
def transactions(request):
  # Pass through relevent data 

  return render(request, 'transactions.html')


@login_required
def budget(request):
  # Pass through relevent data 

  return render(request, 'budget.html')


@login_required
def settings(request):
  # Pass through relevent data 

  return render(request, 'settings.html')


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
