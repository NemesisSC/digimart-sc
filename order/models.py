from django.db import models
from django.contrib.auth.models import User
from cart.models import CartItem, Cart
from products.models import Product


class Order(models.Model):
    ORDER_STATUS = (

        ('PENDING', 'PENDING'),
        ('APPROVED', 'APPROVED'),
        ('REJECTED', 'REJECTED'),
    )
    
    DELIVERY_STATUS = (

        ('PENDING', 'PENDING'),
        ('OUT-FOR-DELIVERY', 'OUT-FOR-DELIVERY'),
        ('DELIVERED', 'DELIVERED'),
        ('DISMISSED', 'DISMISSED')
    )
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=200, choices=ORDER_STATUS, default='PENDING')
    delivery_status = models.CharField(max_length=200, choices=DELIVERY_STATUS, default='PENDING')
    message = models.TextField(null=True, blank=True)
    
    
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        return self.product.price * self.quantity