from django.shortcuts import render, redirect, get_object_or_404
from .models import TargetBudget, ActualBudget, UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import LoginView
from django.contrib.auth import login
from .forms import TargetBudgetForm, ActualBudgetForm
from .models import MONTH_CHOICES
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from datetime import datetime
from calendar import month_name
from django.forms.models import model_to_dict
from django.views.decorators.http import require_http_methods

CURRENT_YEAR = datetime.now().year

class Home(LoginView):
    template_name = 'home.html'


def about(request):
    return render(request, 'about.html')


@login_required
def profile(request):
    user_profile, created = UserProfile.objects.get_or_create(user=request.user)

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
            return redirect('profile')
        else:
            error_message = 'Invalid sign up - try again'

    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'signup.html', context)


@login_required
def target_budget_view(request):
    current_year = datetime.now().year
    current_month = datetime.now().month

    selected_month = int(request.GET.get('month', current_month))
    selected_year = int(request.GET.get('year', current_year))

    month_choices = [(i, month_name[i]) for i in range(1, 13)]
    year_choices = [year for year in range(current_year - 1, current_year + 5)]

    target_budgets = TargetBudget.objects.filter(
        user=request.user,
        month=selected_month,
        year=selected_year
    )

    target_budget_form = TargetBudgetForm(initial={
        'month': selected_month,
        'year': selected_year
    })

    if request.method == 'POST':
        target_budget_form = TargetBudgetForm(request.POST)
        if target_budget_form.is_valid():
            new_budget = target_budget_form.save(commit=False)
            new_budget.user = request.user
            new_budget.save()
            
            return redirect(f"{request.path}?month={selected_month}&year={selected_year}")

    return render(request, 'target_budget/create.html', {
        'target_budgets': target_budgets,
        'target_budget_form': target_budget_form,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'month_choices': month_choices,
        'year_choices': year_choices,
        'current_year': current_year,
    })

@require_http_methods(["GET", "POST"])
@login_required
def edit_target_budget(request, pk):
    target_budget = get_object_or_404(TargetBudget, pk=pk, user=request.user)

    if request.method == 'GET':
        data = model_to_dict(target_budget)
        data['cost_category'] = target_budget.cost_category.id
        data['month'] = target_budget.month 

        return JsonResponse(data)

    elif request.method == 'POST':
        form = TargetBudgetForm(request.POST, instance=target_budget)
        if form.is_valid():
            form.save()

            return redirect('target-budget-view')

        return JsonResponse({'errors': form.errors}, status=400)

@require_http_methods(["DELETE"])
@login_required
def delete_target_budget(request, pk):
    target_budget = get_object_or_404(TargetBudget, pk=pk, user=request.user)
    target_budget.delete()
    return JsonResponse({'success': True})

@login_required
def actual_budget_view(request):
    current_year = datetime.now().year
    current_month = datetime.now().month

    selected_month = request.GET.get('month', current_month)
    selected_year = request.GET.get('year', current_year)

    month_choices = [(i, month_name[i]) for i in range(1, 13)]
    year_choices = [year for year in range(current_year - 1, current_year + 5)]

    actual_budgets = ActualBudget.objects.filter(
        user=request.user,
        month=selected_month,
        year=selected_year
    )

    form = ActualBudgetForm(initial={
        'month': selected_month,
        'year': selected_year
    })

    if request.method == 'POST':
        form = ActualBudgetForm(request.POST)
        if form.is_valid():
            new_budget = form.save(commit=False)
            new_budget.user = request.user
            new_budget.save()
            
            return redirect(f"{request.path}?month={selected_month}&year={selected_year}")

    return render(request, 'actual_budget/create.html', {
        'actual_budgets': actual_budgets,
        'form': form,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'month_choices': month_choices,
        'year_choices': year_choices,
        'current_year': current_year,
    })

@require_http_methods(["GET", "POST"])
@login_required
def edit_actual_budget(request, pk):
    actual_budget = get_object_or_404(ActualBudget, pk=pk, user=request.user)

    if request.method == 'GET':
        data = model_to_dict(actual_budget)
        data['cost_category'] = actual_budget.cost_category.id 
        data['month'] = actual_budget.month 

        return JsonResponse(data)

    elif request.method == 'POST':
        form = ActualBudgetForm(request.POST, instance=actual_budget)
        if form.is_valid():
            form.save()

            return redirect('actual-budget-view')

        return JsonResponse({'errors': form.errors}, status=400)
    

@require_http_methods(["DELETE"])
@login_required
def delete_actual_budget(request, pk):
    actual_budget = get_object_or_404(ActualBudget, pk=pk, user=request.user)
    actual_budget.delete()
    return JsonResponse({'success': True})

@login_required
def budget_comparison_view(request):
    selected_month = request.GET.get('month', 1)
    selected_year = request.GET.get('year', CURRENT_YEAR)

    target_budgets = TargetBudget.objects.filter(user=request.user, month=selected_month, year=selected_year)
    actual_budgets = ActualBudget.objects.filter(user=request.user, month=selected_month, year=selected_year)

    total_target_cost = 0
    total_actual_cost = 0

    comparison_data = []
    for target in target_budgets:
        
        actual_spent = actual_budgets.filter(cost_category=target.cost_category).first()
        actual_value = actual_spent.actual_spent if actual_spent else 0

        variance_amount = actual_value - target.cost_target
        variance_percentage = (variance_amount / target.cost_target * 100) if target.cost_target else 0

        comparison_data.append({
            'category': target.cost_category.name,
            'target': target.cost_target,
            'actual': actual_value,
            'variance_amount': variance_amount,
            'variance_percentage': variance_percentage
        })

        total_target_cost += target.cost_target
        total_actual_cost += actual_value

    comparison_data.append({
        'category': 'Total',
        'target': total_target_cost,
        'actual': total_actual_cost,
        'variance_amount': total_actual_cost - total_target_cost,
        'variance_percentage': ((total_actual_cost - total_target_cost) / total_target_cost * 100) if total_target_cost else 0
    })

    month_choices = [
        (1, 'January'), (2, 'February'), (3, 'March'),
        (4, 'April'), (5, 'May'), (6, 'June'),
        (7, 'July'), (8, 'August'), (9, 'September'),
        (10, 'October'), (11, 'November'), (12, 'December')
    ]
    year_choices = [(i, str(i)) for i in range(CURRENT_YEAR, CURRENT_YEAR + 11)]

    template_name = 'comparisons/data_visualization.html' if 'data-visualization/' in request.path else 'comparisons/report.html'

    return render(request, template_name, {
        'month_choices': month_choices,
        'year_choices': year_choices,
        'selected_month': selected_month,
        'selected_year': selected_year,
        'comparison_data': comparison_data,
        'total_target_cost': total_target_cost,
        'total_actual_cost': total_actual_cost,
    })