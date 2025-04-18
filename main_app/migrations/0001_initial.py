# Generated by Django 5.2 on 2025-04-08 22:20

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(choices=[('operating', 'Operating'), ('employee', 'Employee'), ('marketing', 'Marketing'), ('inventory_supplies', 'Inventory/Supplies'), ('equipment', 'Equipment'), ('repayments_taxes', 'Repayments/Taxes'), ('professional_fees', 'Professional Fees'), ('travel', 'Travel'), ('miscellaneous', 'Miscellaneous')], max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='ActualBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('year', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('actual_spent', models.DecimalField(decimal_places=2, max_digits=10)),
                ('actual_month_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('cost_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.costcategory')),
            ],
        ),
        migrations.CreateModel(
            name='TargetBudget',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('month', models.IntegerField(choices=[(1, 'January'), (2, 'February'), (3, 'March'), (4, 'April'), (5, 'May'), (6, 'June'), (7, 'July'), (8, 'August'), (9, 'September'), (10, 'October'), (11, 'November'), (12, 'December')])),
                ('year', models.IntegerField()),
                ('description', models.TextField(blank=True)),
                ('cost_target', models.DecimalField(decimal_places=2, max_digits=10)),
                ('target_month_income', models.DecimalField(decimal_places=2, max_digits=10)),
                ('date_added', models.DateTimeField(default=django.utils.timezone.now)),
                ('cost_category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.costcategory')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_name', models.CharField(max_length=200)),
                ('email', models.EmailField(max_length=254)),
                ('name', models.CharField(max_length=255)),
                ('date_joined', models.DateTimeField(auto_now_add=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
