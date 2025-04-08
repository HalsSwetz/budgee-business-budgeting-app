from django import forms
from .models import TargetBudget, ActualBudget
from datetime import datetime

CURRENT_YEAR = datetime.now().year
YEAR_CHOICES = [(i, str(i)) for i in range(CURRENT_YEAR, CURRENT_YEAR + 11)]

class TargetBudgetForm(forms.ModelForm):
    class Meta:
        model = TargetBudget
        fields = ['month', 'year', 'cost_category', 'description', 'cost_target', 'target_month_income']

    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select)


class ActualBudgetForm(forms.ModelForm):
    class Meta:
        model = ActualBudget
        fields = ['month', 'year', 'cost_category', 'description', 'actual_spent', 'actual_month_income']

    year = forms.ChoiceField(choices=YEAR_CHOICES, widget=forms.Select)