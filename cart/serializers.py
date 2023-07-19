from django.conf import settings
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from .models import *
from products.serializers import ProductCartSerializer, ProductCartReadSerializer



class CartSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Cart
        fields = '__all__'
        
class CartItemSerializer(serializers.ModelSerializer):
    product = ProductCartSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart', 'product', 'quantity', 'created_at', 'updated_at', 'total_price')
        read_only_fields = ('created_at', 'updated_at', 'total_price')
       
       
class CartItemReadSerializer(serializers.ModelSerializer):
    product = ProductCartReadSerializer(read_only=True)

    class Meta:
        model = CartItem
        fields = ('id', 'cart','product',  'quantity', 'created_at', 'updated_at', 'total_price')
        read_only_fields = ('created_at', 'updated_at', 'total_price') 
        
class CartReadSerializer(serializers.ModelSerializer):
    cartitem_set = CartItemReadSerializer(many=True, read_only=True)
    total_items = serializers.SerializerMethodField()
    total_price = serializers.SerializerMethodField()

    def get_total_items(self, obj):
        return obj.total_items()

    def get_total_price(self, obj):
        return obj.total_price()

    class Meta:
        model = Cart
        fields = ('id', 'user', 'created_at', 'updated_at', 'cartitem_set', 'total_items', 'total_price')
        read_only_fields = ('created_at', 'updated_at', 'total_items', 'total_price')



