# Generated by Django 4.2.6 on 2023-10-27 12:34

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0002_alter_expense_date_alter_expense_user"),
    ]

    operations = [
        migrations.AddField(
            model_name="expense",
            name="subcategory",
            field=models.CharField(
                choices=[
                    ("Gas", "Gas"),
                    ("Fuel", "Fuel"),
                    ("MPK/PKP Tickets", "MPK/PKP Tickets"),
                    ("Taxi", "Taxi"),
                    ("Financial cushion", "Financial cushion"),
                    ("Own contribution", "Own contribution"),
                    ("Investments", "Investments"),
                    ("Others", "Others"),
                ],
                default="Fuel",
                max_length=30,
            ),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name="expense",
            name="date",
            field=models.DateField(default=datetime.date(2023, 10, 27)),
        ),
    ]
