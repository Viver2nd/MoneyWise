from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

INCOMES = (
    ('salary', 'Salary'), ('gift', 'Gift'),
    ('investment', 'Investment'), ('rewards', 'Rewards'),
    ('other', 'Other')
)

EXPENSES = (
    ('clothing', 'Clothing'), ('restaurant', 'Restaurant'),
    ('supermarket', 'Supermarket'), ('home', 'Home'),
    ('travel', 'Travel'), ('transport', 'Transport'), 
    ('other', 'Other')
)

class Account(models.Model):
    name = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('accounts')
    
    def update_balance(self):
        total_income = self.income_set.aggregate(total=models.Sum('amount'))['total'] or 0
        total_expenses = self.expense_set.aggregate(total=models.Sum('amount'))['total'] or 0
        self.balance = total_income - total_expenses
        self.save()
    

class Income(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=INCOMES,
        default=INCOMES[0][0]
    )
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account.name} made {self.amount} on {self.category} at {self.date}"
    
    class Meta:
        ordering = ['-date']
    

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=EXPENSES,
        default=EXPENSES[0][0]
    )
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.account.name} spent {self.amount} on {self.category} at {self.date}"
    
    class Meta:
        ordering = ['-date']


class Budget(models.Model):
    date_from = models.DateField()
    date_to = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Budget from {self.date_from} to {self.date_to}: {self.amount}"