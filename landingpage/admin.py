from django.contrib import admin
from .models import PredictionResult

@admin.register(PredictionResult)
class PredictionResultAdmin(admin.ModelAdmin):
    list_display = ('name', 'predicted_category', 'age', 'gender', 'occupation', 'recommended_products')
    search_fields = ('name', 'predicted_category')
