from rest_framework import serializers
from .models import *
from products.serializers import *
from authentication.serializer import *



class OrderItemSerializer(serializers.Serializer):
    product = ProductCartSerializer(read_only=True)
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'total_price']
    
    
class OrderSerializer(serializers.ModelSerializer):
    
    
    class Meta:
        model = Order
        fields = ['id', 'user',  'total_price', 'created_at']
        
        
class OrderReadSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True)
    
    
    class Meta:
        model = Order
        fields = ['id', 'user','orderitem_set', 'order_status','delivery_status',  'total_price', 'created_at', 'message']
        
class OrderAdminSerializer(serializers.ModelSerializer):
    orderitem_set = OrderItemSerializer(many=True, read_only=True)
    user = serializers.SerializerMethodField('get_user_info')
    
    def get_user_info(self, instance):
        employee_instance = UserInfoSerializer(instance.user).data
        return employee_instance
    
    
    class Meta:
        model = Order
        fields = ['id', 'user','orderitem_set','order_status','delivery_status',  'total_price', 'created_at', 'message']