from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator
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


class ExpenseReportQuerysetSerializer(serializers.Serializer):
    category = serializers.CharField(max_length=40)
    total = serializers.DecimalField(max_digits=8, decimal_places=2)

    class Meta:
        fields = ["category", "total"]


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = ["id", "year", "month", "show_report_url", "data"]
        read_only_fields = ("show_report_url", "data",)
        validators = [
            UniqueTogetherValidator(
                queryset=Report.objects.all(),
                fields=["year", "month"]
            )
        ]

    def validate(self, data):
        # check if the year is unique while there is no month,
        if not data["month"]:
            try:
                instance = Report.objects.get(
                    user=self.context["request"].user,
                    year=data["year"],
                    month=None
                )
            except ObjectDoesNotExist:
                return data
            raise serializers.ValidationError("Report with given data already exists.")
        else:
            return data


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
