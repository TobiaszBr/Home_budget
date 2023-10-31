from django.contrib.auth.models import User
from rest_framework import serializers
from .categories import CATEGORIES, SUBCATEGORIES_DICT
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(
        choices=CATEGORIES,
        style={"template": "templates/expenses/select_onchange_submit.html"},
    )

    class Meta:
        model = Expense
        fields = ["id", "category", "subcategory", "amount", "date", "description"]

    def validate(self, data):
        # Filter available subcategories based on given category - drf view
        self.fields["subcategory"].choices = SUBCATEGORIES_DICT[data["category"]]

        # Validate subcategory with given category
        if (
            not (data["subcategory"], data["subcategory"])
            in SUBCATEGORIES_DICT[data["category"]]
        ):
            raise serializers.ValidationError("Wrong subcategory for chosen category")
        return super().validate(data)


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
