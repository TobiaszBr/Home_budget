from django.contrib.auth.models import User
from django.core.validators import DecimalValidator, MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from .categories import CATEGORIES, SUBCATEGORIES


class Expense(models.Model):
    category = models.CharField(max_length=40, choices=CATEGORIES)
    subcategory = models.CharField(max_length=100, choices=SUBCATEGORIES)
    amount = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        validators=[DecimalValidator(max_digits=6, decimal_places=2),
                    MinValueValidator(limit_value=0)]
    )
    date = models.DateField(default=timezone.now().date())
    user = models.ForeignKey(User, related_name="expenses", on_delete=models.CASCADE)
    description = models.TextField(max_length=100)


# def user_directory_path(instance, filename):
#     # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
#     return f"user_{instance.user.id}/{filename}"


class Report(models.Model):
    user = models.ForeignKey(User, related_name="report", on_delete=models.CASCADE)
    year = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=2000),
            MaxValueValidator(limit_value=3000)
        ]
    )
    month = models.IntegerField(
        validators=[
            MinValueValidator(limit_value=1),
            MaxValueValidator(limit_value=12)
        ]
    )
    #report_pdf = models.FileField(upload_to=user_directory_path)
    report_pdf = models.URLField()
    data = models.JSONField()
