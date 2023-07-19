from django.db import models
from category.models import *
from django.contrib.auth.models import User
# Create your models here.
import uuid
import system_manager.helper

class Product(models.Model):
    pid = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    unit = models.CharField(max_length=200, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.DO_NOTHING, related_name='product_category', null=True)
    featured = models.BooleanField(default=False)
    stock_status = models.BooleanField(default=False)
    hot_items = models.BooleanField(default=False)
    description = models.TextField(null=True)
    sell_description = models.TextField(null=True, blank=True)
    sell_price = models.FloatField()
    on_sale = models.BooleanField(default=False)
    status = models.BooleanField(default=False)
    super_sale = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    


class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(null=True, blank=True)
    parent = models.IntegerField(default=0)
    description = models.TextField(null=True)
    image = models.ImageField(upload_to= generate_filename, null=True, default='default/placeholder.jpeg')  
    featured = models.BooleanField(default=False)
    status = models.BooleanField(default=False)



class ProductUnit(models.Model):
    name = models.CharField(max_length=200)
    created_at = models.DateTimeField(auto_now_add=True)


class ProductImages(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_img')
    image = models.ImageField(upload_to= system_manager.helper.generate_filename)



class ProductUser(models.Model):
    pid = models.CharField(max_length=20, null=True, blank=True)
    product_name = models.CharField(max_length=200)
    owner_name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=255, null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,related_name='user_product', null=True)
    email = models.CharField(max_length=200, null = True)
    phone = models.CharField(max_length=200, null = True)
    approve_status = models.BooleanField(default=False)
    availability_status = models.BooleanField(default=False)
    description = models.TextField(null=True)
    address = models.TextField(null=True)
    sell_price = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to= system_manager.helper.generate_filename, null=True, default='default/placeholder.jpeg')
