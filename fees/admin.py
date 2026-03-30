from django.contrib import admin
from .models import FeeCategory, FeeStructure, Invoice, Transaction


# 🔹 Fee Category
@admin.register(FeeCategory)
class FeeCategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description")
    search_fields = ("name",)


# 🔹 Fee Structure
@admin.register(FeeStructure)
class FeeStructureAdmin(admin.ModelAdmin):
    list_display = ("id", "student_class", "category", "amount", "is_recurring")
    list_filter = ("student_class", "category", "is_recurring")
    search_fields = ("student_class__name", "category__name")


# 🔹 Transaction Inline (inside Invoice)
class TransactionInline(admin.TabularInline):
    model = Transaction
    extra = 0
    readonly_fields = ("date_paid",)


# 🔹 Invoice
@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "student",
        "month",
        "year",
        "total_amount",
        "paid_amount",
        "status",
    )
    list_filter = ("status", "month", "year")
    search_fields = ("student__name",)
    inlines = [TransactionInline]


# 🔹 Transaction
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "invoice",
        "amount_paid",
        "payment_mode",
        "date_paid",
    )
    list_filter = ("payment_mode", "date_paid")
    search_fields = ("invoice__student__name",)