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

    transport_subcategories = [
        ("Gas", "Gas"),
        ("Fuel", "Fuel"),
        ("MPK/PKP Tickets", "MPK/PKP Tickets"),
        ("Taxi", "Taxi")
    ]

    savings_subcategories = [
        ("Financial cushion", "Financial cushion"),
        ("Own contribution", "Own contribution"),
        ("Investments", "Investments"),
        ("Others", "Others")
    ]

    subcategories = transport_subcategories + savings_subcategories

    category = models.CharField(max_length=30, choices=categories)
    subcategory = models.CharField(max_length=30, choices=subcategories, blank=True)
    amount = models.DecimalField(
        blank=True,
        max_digits=6,
        decimal_places=2,
        default=0.0,
        validators=[DecimalValidator(max_digits=6, decimal_places=2),
                    MinValueValidator(limit_value=0)]
    )
    #date = models.DateField(auto_now_add=True)
    date = models.DateField(blank=True, default=datetime.today().date())
    user = models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE)
    description = models.TextField(blank=True, max_length=100)
