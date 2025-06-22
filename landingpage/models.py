from django.db import models

class ProductCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(blank=True, null=True)
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    description = models.TextField(blank=True, null=True)

class PredictionResult(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=50, default='N/A')
    occupation = models.CharField(max_length=100, default='N/A')
    event = models.CharField(max_length=100, default='N/A')
    predicted_category = models.CharField(max_length=100, default='Unknown')
    recommended_products = models.JSONField(default=list)  # Store a list of recommended products

    def __str__(self):
        return self.name

    def generate_recommended_products(self):
        """ Generate recommended products based on predicted category """
        if self.predicted_category == "Electronics":
            return ["Smartphone", "Laptop", "Headphones"]
        elif self.predicted_category == "Clothing":
            return ["T-shirt", "Jeans", "Jacket"]
        else:
            return ["Product 1", "Product 2", "Product 3"]

    def save(self, *args, **kwargs):
        """ Override save to automatically generate recommended products if not set """
        if not self.recommended_products:  # Ensure it's only generated if it's empty
            self.recommended_products = self.generate_recommended_products()
        super().save(*args, **kwargs)
