from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import UpdateView, DeleteView
from .models import TargetBudget, ActualBudget, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import TargetBudgetForm, ActualBudgetForm
from .models import MONTH_CHOICES
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from datetime import datetime
# Create your views here.
CURRENT_YEAR = datetime.now().year

class Home(LoginView):
    template_name = 'home.html'

def about(request):
    return render(request, 'about.html')


def profile(request):
    user_profile = UserProfile.objects.get(user=request.user)

    return render(request, 'profile.html', {
        'user_profile': user_profile
    })


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
    
        if form.is_valid():
            user = form.save()
            UserProfile.objects.create(user=user)
            login(request, user)
            return redirect('profile/')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)



def target_budget_view(request):
    target_budgets = TargetBudget.objects.filter(user=request.user)
    target_budget_form = TargetBudgetForm()

    if request.method == 'POST':
        target_budget_form = TargetBudgetForm(request.POST)
        if target_budget_form.is_valid():
            new_budget = target_budget_form.save(commit=False)
            new_budget.user = request.user
            new_budget.save()
            return redirect('target-budget-view')
        
    return render(request, 'target_budget/create.html', {
        'target_budgets': target_budgets,
        'target_budget_form': target_budget_form,
    })

def edit_target_budget(request, pk):
    target_budget = get_object_or_404(TargetBudget, pk=pk)

    if request.method == 'POST':
        form = TargetBudgetForm(request.POST, instance=target_budget)
        if form.is_valid():
            form.save()
            return redirect('target-budget-view')
    else:
        form = TargetBudgetForm(instance=target_budget)

    return render(request, 'edit_target_budget.html', {'form': form})


def delete_target_budget(request, pk):
    target_budget = get_object_or_404(TargetBudget, pk=pk)
    target_budget.delete()
    return JsonResponse({'success': True})


def actual_budget_view(request):
    actual_budgets = ActualBudget.objects.filter(user=request.user)
    actual_budget_form = ActualBudgetForm()

    if request.method == "POST":
        actual_budget_form = ActualBudgetForm(request.POST)
        if actual_budget_form.is_valid():
            new_budget = actual_budget_form.save(commit=False)
            new_budget.user = request.user
            new_budget.save()
            return redirect('actual-budget')

    return render(request, 'actual_budget/create.html', {
        'actual_budgets': actual_budgets,
        'actual_budget_form': actual_budget_form,
    })

# class ActualBudgetUpdateView(LoginRequiredMixin, UpdateView):
#     model = ActualBudget
#     form_class = ActualBudgetForm
#     template_name = 'actual_budget/edit.html'

#     def get_success_url(self):
#         return reverse_lazy('actual-budget-view')

# class ActualBudgetDeleteView(LoginRequiredMixin, DeleteView):
#     model = ActualBudget
#     template_name = 'actual_budget/delete.html'
#     success_url = reverse_lazy('actual-budget-view')




def budget_comparison_view(request):
    selected_month = request.GET.get('month', 1)
    selected_year = request.GET.get('year', CURRENT_YEAR)

    target_budgets = TargetBudget.objects.filter(user=request.user, month=selected_month, year=selected_year)
    actual_budgets = ActualBudget.objects.filter(user=request.user, month=selected_month, year=selected_year)

    comparison_data = []
    for target in target_budgets:
        actual = actual_budgets.filter(cost_category=target.cost_category).first()
        if actual:
            variance_amount = actual.actual_spent - target.cost_target
            variance_percentage = (variance_amount / target.cost_target) * 100 if target.cost_target != 0 else 0

            comparison_data.append({
                'category': target.cost_category.name,
                'target': target.cost_target,
                'actual': actual.actual_spent,
                'variance_amount': variance_amount,
                'variance_percentage': variance_percentage,
            })
    
    month_choices = MONTH_CHOICES
    year_choices = [(i, str(i)) for i in range(CURRENT_YEAR, CURRENT_YEAR + 11)] 
    
    if 'data-visualization/' in request.path:
        return render(request, 'comparisons/data_visualization.html', {
            'month_choices': month_choices,
            'year_choices': year_choices,
            'selected_month': selected_month,
            'selected_year': selected_year,
            'comparison_data': comparison_data,
        })
    else:
    
        return render(request, 'comparisons/report.html', {
            'month_choices': month_choices,
            'year_choices': year_choices,
            'selected_month': selected_month,
            'selected_year': selected_year,
            'comparison_data': comparison_data,
        })
