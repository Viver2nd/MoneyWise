from django.contrib import admin
from .models import Account, Income, Expense

# Register your models here.
admin.site.register(Account)
admin.site.register(Income)
admin.site.register(Expense)