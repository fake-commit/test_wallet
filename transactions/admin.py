from django.contrib import admin

from .models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ("id", "wallet", "txid", "amount")
    search_fields = ("txid",)
    list_filter = ("wallet",)
    ordering = ("-id",)
