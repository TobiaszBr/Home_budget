from django.contrib.auth.models import User
from django.core.validators import DecimalValidator, MinValueValidator
from django.db import models
from django.forms import ModelForm, Select
from datetime import datetime
from .categories import MAIN_CATEGORIES, SUBCATEGORIES_LIST


class Expense(models.Model):
    category = models.CharField(max_length=40, choices=MAIN_CATEGORIES)
    subcategory = models.CharField(max_length=100, choices=SUBCATEGORIES_LIST)
    amount = models.DecimalField(
        blank=False,
        max_digits=6,
        decimal_places=2,
        default=0.0,
        validators=[DecimalValidator(max_digits=6, decimal_places=2),
                    MinValueValidator(limit_value=0)]
    )
    #date = models.DateField(auto_now_add=True)
    date = models.DateField(default=datetime.today().date())
    user = models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE)
    description = models.TextField(max_length=100)


class ExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = []
        widgets = {
            "category": Select(attrs={"onchange": "this.form.submit();"})
        }
