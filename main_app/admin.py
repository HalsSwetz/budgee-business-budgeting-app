from django.contrib import admin
from .models import TargetBudget, ActualBudget, UserProfile

# Register your models here.

admin.site.register(TargetBudget)
admin.site.register(ActualBudget)
admin.site.register(UserProfile)