from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.

MONTH_CHOICES = [
    (1, 'January'),
    (2, 'February'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
]

class CostCategory(models.Model):
    CATEGORY_CHOICES = [
        ('operating', 'Operating'),
        ('employee', 'Employee'),
        ('marketing', 'Marketing'),
        ('inventory_supplies', 'Inventory/Supplies'),
        ('equipment', 'Equipment'),
        ('repayments_taxes', 'Repayments/Taxes'),
        ('professional_fees', 'Professional Fees'),
        ('travel', 'Travel'),
        ('miscellaneous', 'Miscellaneous'),
    ]
    name = models.CharField(max_length=100, choices=CATEGORY_CHOICES)
    
    def __str__(self):
        return self.get_name_display()


class TargetBudget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()
    cost_category = models.ForeignKey(CostCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    cost_target = models.DecimalField(max_digits=10, decimal_places=2)
    target_month_income = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.cost_category.name} - {self.get_month_display()}/{self.year}"
    

class ActualBudget(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    month = models.IntegerField(choices=MONTH_CHOICES)
    year = models.IntegerField()
    cost_category = models.ForeignKey(CostCategory, on_delete=models.CASCADE)
    description = models.TextField(blank=True)
    actual_spent = models.DecimalField(max_digits=10, decimal_places=2)
    actual_month_income = models.DecimalField(max_digits=10, decimal_places=2)
    date_added = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.cost_category.name} - {self.get_month_display()}/{self.year}"
