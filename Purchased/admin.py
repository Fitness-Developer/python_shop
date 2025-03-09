from django.contrib import admin
from .models import Purchased

class PurchasedAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'price', 'status')  # Добавьте статус в список отображаемых полей

admin.site.register(Purchased, PurchasedAdmin)
