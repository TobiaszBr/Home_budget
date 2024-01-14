from django.contrib import admin
from .models import Expense


class ExpenseAdmin(admin.ModelAdmin):
    fields = ["user", "category", "subcategory", "amount", "date", "description"]


admin.site.register(Expense, ExpenseAdmin)
