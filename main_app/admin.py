from django.contrib import admin
from .models import TargetBudget, ActualBudget, UserProfile, CostCategory

# Register your models here.
admin.site.register(CostCategory)
admin.site.register(TargetBudget)
admin.site.register(ActualBudget)
admin.site.register(UserProfile)