# Generated by Django 4.2.6 on 2023-11-23 15:31

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0018_alter_report_data"),
    ]

    operations = [
        migrations.AddField(
            model_name="report",
            name="report_save_path",
            field=models.FilePathField(default=None),
            preserve_default=False,
        ),
    ]