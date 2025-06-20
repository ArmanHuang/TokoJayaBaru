from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home page URL
    path('polls/', views.polls, name='landingpage_polls'),  # Poll form URL
    path('get-products/<str:category_name>/', views.get_products_by_category, name='get_products'),

]
