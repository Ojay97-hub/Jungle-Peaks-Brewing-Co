from django.contrib import admin
from .models import Product, Category, Review

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
    
class ReviewAdmin(admin.ModelAdmin):  # New admin class for Reviews
    list_display = ('product', 'user', 'rating', 'comment', 'created_at')
    list_filter = ('rating', 'product')
    search_fields = ('user__username', 'product__name', 'comment')

admin.site.register(Product, ProductAdmin) 
admin.site.register(Category, CategoryAdmin) 
admin.site.register(Review, ReviewAdmin)  # Register the Review model