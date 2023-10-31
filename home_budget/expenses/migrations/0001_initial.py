# Generated by Django 4.2.6 on 2023-10-23 18:10

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Expense",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "category",
                    models.CharField(
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
                (
                    "amount",
                    models.DecimalField(
                        decimal_places=2,
                        default=0.0,
                        max_digits=6,
                        validators=[
                            django.core.validators.DecimalValidator(
                                decimal_places=2, max_digits=6
                            ),
                            django.core.validators.MinValueValidator(limit_value=0),
                        ],
                    ),
                ),
                ("date", models.DateField(auto_now_add=True)),
                ("description", models.TextField(max_length=100)),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
