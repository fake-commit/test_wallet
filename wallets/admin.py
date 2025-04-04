from django.contrib import admin

from .models import Wallet


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ("id", "label", "balance")
    search_fields = ("label",)
    ordering = ("label",)
