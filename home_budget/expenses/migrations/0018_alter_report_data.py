# Generated by Django 4.2.6 on 2023-11-23 10:36

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0017_report_data"),
    ]

    operations = [
        migrations.AlterField(
            model_name="report",
            name="data",
            field=models.JSONField(),
        ),
    ]
