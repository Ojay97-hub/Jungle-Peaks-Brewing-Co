from django.contrib import admin
from .models import Product, Category

# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'category',
        'price',
        'rating',
        'sku',
        'has_sizes',
    )
    ordering = ('sku',)
    list_filter = ('has_sizes', 'category')

class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'name',
    )

admin.site.register(Product, ProductAdmin) 
admin.site.register(Category, CategoryAdmin) 