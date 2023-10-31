from django.contrib import admin
from .models import Expense, ExpenseForm


class ExpenseAdmin(admin.ModelAdmin):
    form = ExpenseForm
    fields = ["category", "subcategory", "amount", "date", "description"]


admin.site.register(Expense, ExpenseAdmin)
