from django.contrib.auth.models import User
from django.core.validators import DecimalValidator, MinValueValidator
from django.db import models
from django.forms import ModelForm, Select
from django.utils import timezone
from .categories import CATEGORIES, SUBCATEGORIES


class Expense(models.Model):
    category = models.CharField(max_length=40, choices=CATEGORIES)
    subcategory = models.CharField(max_length=100, choices=SUBCATEGORIES)
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[DecimalValidator(max_digits=6, decimal_places=2),
                    MinValueValidator(limit_value=0)]
    )
    date = models.DateField(default=timezone.now().date())
    user = models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE)
    description = models.TextField(max_length=100)


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = []
        widgets = {
            "category": Select(attrs={"onchange": "this.form.submit();"})
        }
