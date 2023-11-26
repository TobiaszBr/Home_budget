# Generated by Django 4.2.6 on 2023-11-23 16:37

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0023_rename_report_pdf_report_show_report_url"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="month",
            field=models.IntegerField(
                blank=True,
                null=True,
                validators=[
                    django.core.validators.MinValueValidator(limit_value=1),
                    django.core.validators.MaxValueValidator(limit_value=12),
                ],
            ),
        ),
    ]