from django.db import models
from store.models import Product, Variation

# Create your models here.
class Payment(models.Model):
    payment_id = models.CharField(max_length=100, unique=True)
    order_number = models.CharField(max_length=50, default='0000000000')
    payment_method = models.CharField(max_length=100)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2) 
    currency = models.CharField(max_length=10, default='EUR')
    status = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Payment {self.payment_id} - {self.status}"
    
    
class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'), 
        ('Completed', 'Completed'), 
        ('Cancelled', 'Cancelled'),
    )
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    order_number = models.CharField(max_length=20)
    name = models.CharField (max_length=50)
    email = models.EmailField(max_length=50)
    address = models.CharField(max_length=50)
    order_total = models.FloatField(default=0.0)
    status = models.CharField(max_length=10, choices=STATUS, default= 'New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self) :
        return self.name
    
    
class OrderProduct (models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.SET_NULL, blank=True, null=True)
    product = models.ForeignKey (Product, on_delete=models.CASCADE)
    variation = models.ForeignKey(Variation, on_delete=models.CASCADE)
    color = models.CharField(max_length=50)
    size = models.CharField(max_length=50)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

def __str__(self) :
    return self.product.product_name