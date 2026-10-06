from django.contrib import admin
from .models import Category, BakeryItem, CustomOrderRequest


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(BakeryItem)
class BakeryItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'is_available')
    list_filter = ('category', 'is_available')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(CustomOrderRequest)
class CustomOrderRequestAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer_name', 'event_date', 'fulfillment_type', 'status', 'quoted_amount')
    list_filter = ('status', 'fulfillment_type', 'event_date')
    search_fields = ('customer_name', 'email', 'phone')