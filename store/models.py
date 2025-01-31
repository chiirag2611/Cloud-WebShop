from tkinter import CASCADE
from django.db import models
from category.models import Category
from django.urls import reverse

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.IntegerField()
    images          = models.ImageField(upload_to='photos/products')
    stock           = models.IntegerField()
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('product_detail', args=[self.category.slug, self.slug])
    
    
    def __str__(self):
        return self.product_name
    
    
from django.db import models

class Payment(models.Model):
    payment_id = models.CharField(max_length=100, unique=True)
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2)  # Total amount paid
    currency = models.CharField(max_length=10, default='EUR')
    status = models.CharField(max_length=100)  # "Completed", "Failed", etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"


class VariationManager(models.Manager):
    def colors(self):
        return self.filter(variation_category='color', is_active=True)


    
variation_category_choice = (
    ('color', 'color'),
)
    
class Variation(models.Model):
    product = models.ForeignKey(Product, on_delete = models.CASCADE)
    variation_category = models.CharField(max_length=100, choices=variation_category_choice)
    variation_value = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)   
    created_date = models.DateTimeField(auto_now=True)
    
    objects = VariationManager()
    
    def __str__(self):
        return str(self.variation_value)    