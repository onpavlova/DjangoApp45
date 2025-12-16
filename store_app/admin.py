from django.contrib import admin
from django.forms import DecimalField
from decimal import Decimal

from .models import Product, Category


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name','description','price', 'category']
    ordering = ('name',)
    list_filter = ('price',)
    search_fields = ('name','description')
    search_help_text = 'Введите часть заголовка или описания'

    fields = ('name','description','price', 'category')
    @admin.action(description='Изменение цены')
    def price_up(self, request, queryset):
        for product in queryset:
            product.price *= Decimal('1.05')
            product.save()
    actions = (price_up,)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'description']
    ordering = ('name',)
    search_fields = ('name', 'description')
    search_help_text = 'Введите часть заголовка или описания'