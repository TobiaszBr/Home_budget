from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from rest_framework import serializers
from .categories import SUBCATEGORIES_DICT
from .models import Expense, Report


class ExpenseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = ["id", "category", "subcategory", "amount", "date", "description"]

    def validate(self, data):
        # Validate given category with actual subcategory
        if "category" in data.keys() and "subcategory" not in data.keys():
            actual_subcategory = self.context["object_instance"].subcategory
            if actual_subcategory not in SUBCATEGORIES_DICT[data["category"]]:
                raise serializers.ValidationError(
                    "Given category does not match actual subcategory")

        # Validate given subcategory with actual category
        if "subcategory" in data.keys() and "category" not in data.keys():
            actual_category = self.context["object_instance"].category
            if data["subcategory"] not in SUBCATEGORIES_DICT[actual_category]:
                raise serializers.ValidationError(
                    "Given subcategory does not match actual category")

        # Validate given subcategory with given category
        if "category" in data.keys() and "subcategory" in data.keys():
            # Filter available subcategories based on given category - drf view
            if data["subcategory"] not in SUBCATEGORIES_DICT[data["category"]]:
                raise serializers.ValidationError(
                    "Wrong subcategory for chosen category")

        return super().validate(data)


class ExpenseReportSerializer(serializers.Serializer):
    year = serializers.CharField(max_length=4)
    month = serializers.CharField(max_length=2)
    report_pdf = serializers.URLField(allow_blank=True)
    data = serializers.JSONField(allow_null=True)

    class Meta:
        fields = ["year", "month", "report_pdf", "data"]


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["year", "month", "report_pdf", "data"]


class UserSerializer(serializers.ModelSerializer):
    expenses = ExpenseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email",
            "is_staff",
            "expenses",
        ]
