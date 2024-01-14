from django.contrib import admin
from .models import Expense, Report


class ExpenseAdmin(admin.ModelAdmin):
    fields = ["user", "category", "subcategory", "amount", "date", "description"]


class ReportAdmin(admin.ModelAdmin):
    fields = ["user", "year", "month", "report_pdf", "data"]


admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Report, ReportAdmin)
