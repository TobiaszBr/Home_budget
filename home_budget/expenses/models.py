from django.contrib.auth.models import User
from django.db import models
from django.core.validators import DecimalValidator, MinValueValidator
from datetime import datetime


class Expense(models.Model):
    categories = [
        ("Savings", "Savings"),
        ("Food", "Food"),
        ("Flat rent", "Flat rent"),
        ("Multimedia fees", "Multimedia fees"),
        ("Transport", "Transport"),
        ("Fund costs", "Fund costs"),
        ("Others", "Others"),
        ("Loans to others", "Loans to others")
    ]

    category = models.CharField(max_length=30, choices=categories)
    amount = models.DecimalField(
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
