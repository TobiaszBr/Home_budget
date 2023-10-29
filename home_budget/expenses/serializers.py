from django.contrib.auth.models import User
from rest_framework import serializers
from .categories import MAIN_CATEGORIES, SUBCATEGORIES
from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):
    category = serializers.ChoiceField(
        choices=MAIN_CATEGORIES,
        style={"template": "templates/expenses/select_onchange_submit.html"}
    )
    # subcategory = serializers.ChoiceField(
    #     choices=SUBCATEGORIES["Savings"],
    # )
    description = serializers.CharField(
        max_length=100,
        style={"base_template": "textarea.html"},
        allow_blank=True
    )

    # Jeżeli mam to pokomentowane to działa dodawanie na PUT i PATCH itd ale za 1 załadowaniem strony
    # Subcategory zawiera wszystko.. Jeżeli odkomentuje, to bd zawierać tylko startowe Savings
    # ale za to nie działa PUT itd.. bo jest jakiś błąd "\"Grocerise\" np ..
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #self.fields["subcategory"].choices = SUBCATEGORIES["Savings"]

    class Meta:
        model = Expense
        fields = ["id", "category", "subcategory", "amount", "date", "description"]

    def validate(self, data):
        self.fields["subcategory"].choices = SUBCATEGORIES[data["category"]]
        print(data["subcategory"])

        if not (data["subcategory"], data["subcategory"]) in SUBCATEGORIES[data["category"]]:
            raise serializers.ValidationError("Wrong subcategory for choosen category")
        return super().validate(data)


class UserSerializer(serializers.ModelSerializer):
    expenses = ExpenseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "is_staff",
                  "expenses"]
