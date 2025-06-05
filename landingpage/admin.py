# admin.py
from django.urls import path
from django.contrib import admin
from django.utils.html import format_html
from .models import PredictionResult, Product, ProductCategory
from django.http import HttpResponseRedirect
from django.shortcuts import render

@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'predicted_category', 'age', 'gender', 'occupation', 'get_recommended_products'
    )
    search_fields = ('name', 'predicted_category')
    list_filter = ('predicted_category', 'gender', 'occupation')
    list_per_page = 5
    actions = ['print_selected']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print_selected/', self.admin_site.admin_view(self.print_selected_view), name='result_print_selected'),
        ]
        return custom_urls + urls

    def print_selected(self, request, queryset):
        ids = queryset.values_list('id', flat=True)
        ids_str = ",".join(str(i) for i in ids)
        return HttpResponseRedirect(f'print_selected/?ids={ids_str}')
    print_selected.short_description = "Print selected Prediction Results"

    def print_selected_view(self, request):
        ids = request.GET.get('ids')
        if not ids:
            return HttpResponseRedirect("../")  # Redirect ke list jika tidak ada ID

        ids_list = [int(i) for i in ids.split(",")]
        items = PredictionResult.objects.filter(id__in=ids_list)

        return render(request, 'print/predictResult.html', {'items': items})

    def get_recommended_products(self, obj):
        return ", ".join([p for p in obj.recommended_products])  # Adjust if it's ManyToMany
    get_recommended_products.short_description = 'Recommended Products'


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'image_tag', 'description')
    search_fields = ('name',)
    ordering = ('name',)
    list_per_page = 5 
    actions = ['print_selected']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print_selected/', self.admin_site.admin_view(self.print_selected_view), name='category_print_selected'),
        ]
        return custom_urls + urls

    def print_selected(self, request, queryset):
        ids = queryset.values_list('id', flat=True)
        ids_str = ",".join(str(i) for i in ids)
        return HttpResponseRedirect(f'print_selected/?ids={ids_str}')
    print_selected.short_description = "Print selected Product Category"

    def print_selected_view(self, request):
        ids = request.GET.get('ids')
        if not ids:
            return HttpResponseRedirect("../")

        ids_list = [int(i) for i in ids.split(",")]
        items = ProductCategory.objects.filter(id__in=ids_list)

        return render(request, 'print/productCategory.html', {'items': items})
    
    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" style="object-fit: cover; border-radius: 5px;" />', obj.image.url)
        return "-"
    image_tag.short_description = 'Image'

# @admin.register(ProductCategory)
# class ProductCategoryAdmin(admin.ModelAdmin):
#     list_display = ('id', 'category_name', 'subcategory', 'deskcription')  
#     search_fields = ('category_name', 'subcategory')  
#     ordering = ('category_name',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'image_preview', 'description')
    search_fields = ('name',)
    list_filter = ('category',)
    autocomplete_fields = ('category',)
    readonly_fields = ('image_preview',)
    list_per_page = 5
    actions = ['print_selected']

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('print_selected/', self.admin_site.admin_view(self.print_selected_view), name='product_print_selected'),
        ]
        return custom_urls + urls

    def print_selected(self, request, queryset):
        ids = queryset.values_list('id', flat=True)
        ids_str = ",".join(str(i) for i in ids)
        return HttpResponseRedirect(f'print_selected/?ids={ids_str}')
    print_selected.short_description = "Print selected Products"

    def print_selected_view(self, request):
        ids = request.GET.get('ids')
        if not ids:
            return HttpResponseRedirect("../")

        ids_list = [int(i) for i in ids.split(",")]
        items = Product.objects.filter(id__in=ids_list)

        return render(request, 'print/product.html', {'items': items}) 

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="100" height="100" style="object-fit: contain; border-radius: 5px; background-color: #f0f0f0;" />',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'
