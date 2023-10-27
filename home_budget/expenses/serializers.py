from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Expense

categories = [
    ("Savings", "Savings"),
    ("Food", "Food"),
    ("Flat rent", "Flat rent"),
    ("Multimedia fees", "Multimedia fees"),
    ("Transport", "Transport"),
    ("Fund costs", "Fund costs"),
    ("Others", "Others"),
    ("Loans to others", "Loans to others")
]

transport_subcategories = [
    ("Gas", "Gas"),
    ("Fuel", "Fuel"),
    ("MPK/PKP Tickets", "MPK/PKP Tickets"),
    ("Taxi", "Taxi")
]

savings_subcategories = [
    ("Financial cushion", "Financial cushion"),
    ("Own contribution", "Own contribution"),
    ("Investments", "Investments"),
    ("Others", "Others")
]


class ExpenseSerializer(serializers.ModelSerializer):
    subcategory = serializers.ChoiceField(choices=[], allow_blank=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # self.transport_subcategories = [
        #     ("Gas", "Gas"),
        #     ("Fuel", "Fuel"),
        #     ("MPK/PKP Tickets", "MPK/PKP Tickets"),
        #     ("Taxi", "Taxi")
        # ]
        #
        # self.fields["subcategory"].choices = self.transport_subcategories



    class Meta:
        model = Expense
        fields = ["id", "category", "subcategory", "amount", "date", "description"]


    def validate(self, data):
        if data["category"] == "Transport":
            self.fields["subcategory"].choices = transport_subcategories
            self.fields["subcategory"].allow_blank = False
        return super().validate(data)













    # def validate(self, data):
    #     """Checks if subcategory matches appropriate category"""
    #
    #     if data["category"] == "Savings" and data["subcategory"] not in ["Financial cushion", "Own contribution", "Investments", "Others"]:
    #         raise serializers.ValidationError("Subcategory for category 'Savings' can be one of the following: Financial cushion, Own contribution, Investments, Others")
    #     if data["category"] == "Transport" and data["subcategory"] not in ["Gas", "Fuel", "MPK/PKP Tickets", "Taxi"]:
    #         raise serializers.ValidationError("Subcategory for category 'Transport' can be one of the following: Gas, Fuel, MPK/PKP Tickets, Taxi")


class UserSerializer(serializers.ModelSerializer):
    expenses = ExpenseSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "first_name", "last_name", "email", "is_staff",
                  "expenses"]
