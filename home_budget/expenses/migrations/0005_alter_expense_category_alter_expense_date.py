# Generated by Django 4.2.6 on 2023-10-29 16:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0004_alter_expense_amount_alter_expense_date_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="category",
            field=models.CharField(
                blank=True,
                choices=[
                    ("Savings", "Savings"),
                    ("Food", "Food"),
                    ("Flat rent", "Flat rent"),
                    ("Multimedia fees", "Multimedia fees"),
                    ("Transport", "Transport"),
                    ("Fund costs", "Fund costs"),
                    ("Others", "Others"),
                    ("Loans to others", "Loans to others"),
                ],
                max_length=30,
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateField(blank=True, default=datetime.date(2023, 10, 29)),
        ),
    ]
