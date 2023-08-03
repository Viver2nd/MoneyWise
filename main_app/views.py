from django.shortcuts import render, redirect

def dashboard(request):
  # Pass through relevent data 
  
  return render(request, 'dashboard.html')

def accounts(request):
  # Pass through relevent data 

  return render(request, 'accounts.html')

def transactions(request):
  # Pass through relevent data 

  return render(request, 'transactions.html')

def budget(request):
  # Pass through relevent data 

  return render(request, 'budget.html')

def settings(request):
  # Pass through relevent data 

  return render(request, 'settings.html')

