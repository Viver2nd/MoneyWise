from django.forms import ModelForm
from .models import Account, Income, Expense


class IncomeForm(ModelForm):
  class Meta:
    model = Income
    fields = ['amount', 'category', 'description', 'account']

  def __init__(self, user, *args, **kwargs):
    super(IncomeForm, self).__init__(*args, **kwargs)
    self.fields['account'].queryset = Account.objects.filter(user=user)


class ExpenseForm(ModelForm):
  class Meta:
    model = Expense
    fields = ['amount', 'category', 'description', 'account']

  def __init__(self, user, *args, **kwargs):
    super(ExpenseForm, self).__init__(*args, **kwargs)
    self.fields['account'].queryset = Account.objects.filter(user=user)