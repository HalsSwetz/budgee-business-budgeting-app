from django.urls import path
from . import views


urlpatterns = [
    path('', views.Home.as_view(), name='home'),
    path('about/', views.about, name='about'),
    path('profile/', views.profile, name='profile'),
    path('target-budget/', views.target_budget_view, name='target-budget-view'),
    # path('target-budget/<int:pk>/', views.target_budget_detail, name='target-budget-detail'),
    path('target-budget/create/', views.target_budget_view, name='target-budget-create'),
    # path('target-budget/<int:pk>/edit/', views.target_budget_edit, name='target-budget-edit'),
    # path('target-budget/<int:pk>/delete/', views.target_budget_delete, name='target-budget-delete'),
    path('actual-budget/', views.actual_budget_view, name='actual-budget-view'),
    # path('actual-budget/<int:pk>/', views.actual_budget_detail, name='actual-budget-detail'),
    path('actual-budget/create/', views.actual_budget_view, name='actual-budget-create'),
    # path('actual-budget/<int:pk>/edit/', views.actual_budget_edit, name='actual-budget-edit'),
    # path('actual-budget/<int:pk>/delete/', views.actual_budget_delete, name='actual-budget-delete'),
    path('comparisons/report/', views.budget_comparison_view, name='budget-comparison-view'),
    path('comparisons/data-visualization/', views.budget_comparison_view, name='budget-comparison-visualization'),
    path('accounts/signup/', views.signup, name='signup'),
]


