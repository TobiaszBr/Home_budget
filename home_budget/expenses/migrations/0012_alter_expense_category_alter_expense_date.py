# Generated by Django 4.2.6 on 2023-11-03 12:48

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0011_alter_expense_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="category",
            field=models.CharField(
                choices=[
                    ("Savings", "Savings"),
                    ("Food", "Food"),
                    ("Flat rent", "Flat rent"),
                    ("Multimedia fees", "Multimedia fees"),
                    ("Transport", "Transport"),
                    ("Loans", "Loans"),
                    ("Fund costs", "Fund costs"),
                    ("Company expenses", "Company expenses"),
                    ("My loans to others", "My loans to others"),
                    ("Others", "Others"),
                ],
                max_length=40,
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateField(default=datetime.date(2023, 11, 3)),
        ),
    ]