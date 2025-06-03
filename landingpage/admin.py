# admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import PredictionResult, Product, ProductCategory

@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'predicted_category', 'age', 'gender', 'occupation', 'get_recommended_products'
    )
    search_fields = ('name', 'predicted_category')
    list_filter = ('predicted_category', 'gender', 'occupation')

    def get_recommended_products(self, obj):
        return ", ".join([p for p in obj.recommended_products])  # Adjust if it's ManyToMany
    get_recommended_products.short_description = 'Recommended Products'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)
    ordering = ('name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image_preview')
    search_fields = ('name',)
    list_filter = ('category',)
    autocomplete_fields = ('category',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit: cover; border-radius: 5px;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'
