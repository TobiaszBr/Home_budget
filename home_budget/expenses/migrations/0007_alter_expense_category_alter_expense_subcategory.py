# Generated by Django 4.2.6 on 2023-10-29 18:38

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("expenses", "0006_alter_expense_amount_alter_expense_category_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="expense",
            name="category",
            field=models.CharField(
                choices=[
                    ("Savings", "Savings"),
                    ("Food", "Food"),
                    ("Flat rent", "Flat rent"),
                    ("Multimedia fees", "Multimedia fees"),
                    ("Transport", "Transport"),
                    ("Loans to others", "Loans to others"),
                    ("Fund costs", "Fund costs"),
                    ("Company expenses", "Company expenses"),
                    ("My loans to others", "My loans to others"),
                    ("Others", "Others"),
                ],
                max_length=40,
            ),
        ),
        migrations.AlterField(
            model_name="expense",
            name="subcategory",
            field=models.CharField(
                choices=[
                    ("Financial cushion", "Financial cushion"),
                    ("Own contribution", "Own contribution"),
                    ("Investments", "Investments"),
                    ("Others", "Others"),
                    ("Groceries", "Groceries"),
                    ("Fast food", "Fast food"),
                    ("Eating out", "Eating out"),
                    ("Others", "Others"),
                    ("Flat rent", "Flat rent"),
                    ("Billings", "Billings"),
                    ("Others", "Others"),
                    ("Phone", "Phone"),
                    ("Stream platforms", "Stream platforms"),
                    ("Internet", "Internet"),
                    ("Others", "Others"),
                    ("Gas", "Gas"),
                    ("Fuel", "Fuel"),
                    ("Parking", "Parking"),
                    ("Car wash", "Car wash"),
                    ("MPK/PKP Tickets", "MPK/PKP Tickets"),
                    ("Taxi", "Taxi"),
                    ("Others", "Others"),
                    ("Loan", "Loan"),
                    ("Mortgage", "Mortgage"),
                    ("Others", "Others"),
                    ("Health care", "Health care"),
                    ("Suplements", "Suplements"),
                    ("Cleaning stuff", "Cleaning stuff"),
                    ("Flat equipment, tools", "Flat equipment, tools"),
                    ("Laundry stuff", "Laundry stuff"),
                    ("Clothes", "Clothes"),
                    ("Parking Cracow area", "Parking Cracow area"),
                    ("Car repairs, accessories", "Car repairs, accessories"),
                    (
                        "Car's inspections and insurance",
                        "Car's inspections and insurance",
                    ),
                    ("Hygiene products", "Hygiene products"),
                    ("Cosmetics and jewelry", "Cosmetics and jewelry"),
                    (
                        "Beauty treatments, hairdresser",
                        "Beauty treatments, hairdresser",
                    ),
                    ("Work - nail costs", "Work - nail costs"),
                    ("Work - school costs", "Work - school costs"),
                    ("Work - eyebrows costs", "Work - eyebrows costs"),
                    ("Gifts", "Gifts"),
                    ("Special family events", "Special family events"),
                    ("Dates", "Dates"),
                    ("Party fund", "Party fund"),
                    ("Holiday fund", "Holiday fund"),
                    ("1-st November", "1-st November"),
                    ("Charity", "Charity"),
                    ("Others", "Others"),
                    ("Others", "Others"),
                    ("Others", "Others"),
                    ("Others", "Others"),
                ],
                max_length=100,
            ),
        ),
    ]
