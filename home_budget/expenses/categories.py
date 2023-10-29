MAIN_CATEGORIES = [
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
]

SAVINGS = [
    ("Financial cushion", "Financial cushion"),
    ("Own contribution", "Own contribution"),
    ("Investments", "Investments"),
    ("Others", "Others")
]

FOOD = [
    ("Groceries", "Groceries"),
    ("Fast food", "Fast food"),
    ("Eating out", "Eating out"),
    ("Others", "Others")
]

FLAT_RENT = [
    ("Flat rent", "Flat rent"),
    ("Billings", "Billings"),
    ("Others", "Others")
]

MULTIMEDIA_FEES = [
    ("Phone", "Phone"),
    ("Stream platforms", "Stream platforms"),
    ("Internet", "Internet"),
    ("Others", "Others")
]

TRANSPORT = [
    ("Gas", "Gas"),
    ("Fuel", "Fuel"),
    ("Parking", "Parking"),
    ("Car wash", "Car wash"),
    ("MPK/PKP Tickets", "MPK/PKP Tickets"),
    ("Taxi", "Taxi"),
    ("Others", "Others")
]

LOANS_TO_OTHERS = [
    ("Loan", "Loan"),
    ("Mortgage", "Mortgage"),
    ("Others", "Others")
]

FUND_COSTS = [
    ("Health care", "Health care"),
    ("Suplements", "Suplements"),
    ("Cleaning stuff", "Cleaning stuff"),
    ("Flat equipment, tools", "Flat equipment, tools"),
    ("Laundry stuff", "Laundry stuff"),
    ("Clothes", "Clothes"),
    ("Parking Cracow area", "Parking Cracow area"),
    ("Car repairs, accessories", "Car repairs, accessories"),
    ("Car's inspections and insurance", "Car's inspections and insurance"),
    ("Hygiene products", "Hygiene products"),
    ("Cosmetics and jewelry", "Cosmetics and jewelry"),
    ("Beauty treatments, hairdresser", "Beauty treatments, hairdresser"),
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
    ("Others", "Others")
]

COMPANY_EXPENSES = [
    ("Others", "Others")
]

MY_LOANS_TO_OTHERS = [
    ("Others", "Others")
]

OTHERS = [
    ("Others", "Others")
]

SUBCATEGORIES = {
    "Savings": SAVINGS,
    "Food": FOOD,
    "Flat rent": FLAT_RENT,
    "Multimedia fees": MULTIMEDIA_FEES,
    "Transport": TRANSPORT,
    "Loans to others": LOANS_TO_OTHERS,
    "Fund costs": FUND_COSTS,
    "Company expenses": COMPANY_EXPENSES,
    "My loans to others": MY_LOANS_TO_OTHERS,
    "Others": OTHERS
}

SUBCATEGORIES_LIST = [item for element in SUBCATEGORIES.values() for item in element]
