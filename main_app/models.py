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

ACCOUNTS = (
    ('HSBC', 'HSBC'),
    ('Barclays', 'Barclays'),
    ('Lloyds', 'Lloyds'),
    ('NatWest', 'NatWest'),
    ('Santander', 'Santander'),
    ('TSB', 'TSB'),
    ('Nationwide', 'Nationwide'),
    ('Halifax', 'Halifax'),
    ('Metro-Bank', 'Metro-Bank'),
)

class Account(models.Model):
    name = models.CharField(
        max_length=20,
        choices=ACCOUNTS,
        default=ACCOUNTS[0][0]
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def __str__(self):
        return f'{self.name}: £{self.balance}'
    
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
    description = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"You gained £{self.amount} in your {self.account.name} account through {self.category} at {self.date}"
    
    def get_absolute_url(self):
        return reverse('incomes')
    
    class Meta:
        ordering = ['-date']
    

class Expense(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=EXPENSES,
        default=EXPENSES[0][0]
    )
    description = models.TextField(max_length=250)
    date = models.DateTimeField(auto_now_add=True)
    account = models.ForeignKey(Account, on_delete=models.CASCADE)

    def __str__(self):
        return f"You spent £{self.amount} with your {self.account.name} account on {self.category} at {self.date}"
    
    def get_absolute_url(self):
        return reverse('expenses')

    class Meta:
        ordering = ['-date']


class Budget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Monthly Budget: {self.amount}"
    
    def get_absolute_url(self):
        return reverse('budget')