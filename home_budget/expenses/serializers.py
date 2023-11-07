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
        # To tymczasowo - trzeba zrobić tak, żeby sprawdzało zarówno dane wejściowe jeżeli są obie category i subcategory
        # oraz musi sprawdzać możliwość zmiany jednego z nich i porównywać z tym co jest w modelu dla innego pola np jeżeli mam w danych category to
        # sprawdzić z tym co jest w modelu dla subcategories. - ale zmiana jednego pola zawsze bd powodowała błąd, bo jeżeli mam już model zapisany,
        # to tam category i sub sąze sobą ok, zmieniając tylko jedno byłby błąd więc zmiana jednego pola jest niemożliwa. Albo oba na raz albo wcale
        if "category" in data.keys() and "subcategory" in data.keys():
            self.fields["subcategory"].choices = SUBCATEGORIES_DICT[data["category"]]
            # Validate subcategory with given category
            if (
                    not (data["subcategory"], data["subcategory"])
                    in SUBCATEGORIES_DICT[data["category"]]
            ):
                raise serializers.ValidationError(
                    "Wrong subcategory for chosen category")

        # temp do testów
        if "object_instance" in self.context.keys():
            print(self.context["object_instance"].category)

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
