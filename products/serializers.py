from django.conf import settings
from rest_framework import serializers
from rest_framework_friendly_errors.mixins import FriendlyErrorMessagesMixin
from .models import *
from category.serializers import *
from authentication.serializer import *


class ProductInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'
        
class ProductUserSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductUser
        fields = '__all__'

class ProductUserReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    created_by = serializers.SerializerMethodField('get_user_info')
    
    def get_user_info(self, instance):
        user_instance = UserInfoSerializer(instance.created_by).data
        return user_instance
    
    class Meta:
        model = ProductUser
        fields = '__all__'
        
               
class ProductCartSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    
    class Meta:
        model = Product
        fields = (
            'id', 'pid', 'name', 'sell_price'
        )

class ProductCartReadSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    
    
    def get_images(self, instance):
        image_urls = []
        product_images = ProductImages.objects.filter(product=instance)
        if product_images.exists():
            for image in product_images:
                image_urls.append(image.image.url)
        else:
            image_urls.append(self.context['request'].build_absolute_uri('/media/default/placeholder.jpeg'))
        return image_urls
    
    class Meta:
        model = Product
        fields = (
            'id', 'pid', 'name', 'sell_price', 'images'
        )


class ProductUnitSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductUnit
        fields = '__all__'


class ProductImageSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    class Meta:
        model = ProductImages
        fields = '__all__'


class ProductReadInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    category = serializers.SerializerMethodField('get_category')
    subcategory = serializers.SerializerMethodField('get_subcategory')

    def get_category(self, instance):
        try:
            return {
                'name': instance.category.name,
                'slug': instance.category.slug
            }
        except Exception:
            return {
                'name': '',
                'slug': ''
            }

    def get_subcategory(self, instance):
        try:
            return {
                'name': instance.subcategory.name,
                'slug': instance.subcategory.slug
            }
        except Exception:
            return {
                'name': '',
                'slug': ''
            }

    def get_images(self, instance):
        image_urls = []
        images_list = ProductImageSerializer(instance.product_img.all(), many=True,
                                             context={'request': self.context['request']}).data
        if len(images_list) > 0:
            for img in images_list:
                image_urls.append(img['image'])
        else:
            image_urls.append(
                'http://%s/media/default/placeholder.jpeg' % (self.context['request']).META.get('HTTP_HOST'))
        return image_urls

    class Meta:
        model = Product
        fields = (
            'id', 'pid', 'name', 'slug', 'unit', 'featured', 'hot_items', 'description',
            'sell_description',  'sell_price', 'on_sale',
             'status', 'super_sale',  'images', 'category', 'subcategory',
            'created_at', 'updated_at'
        )


class ProductReadTestInfoSerializer(FriendlyErrorMessagesMixin, serializers.ModelSerializer):
    images = serializers.SerializerMethodField('get_images')
    category = serializers.SerializerMethodField('get_category')
    subcategory = serializers.SerializerMethodField('get_subcategory')

   

    def get_category(self, obj):
        category_instance = Category.objects.get(id = obj.category.id)
        return CategorySerializer(category_instance).data

    def get_subcategory(self, instance):
        try:
            return {
                'name': instance.subcategory.name,
                'slug': instance.subcategory.slug
            }
        except Exception:
            return {
                'name': '',
                'slug': ''
            }

    def get_images(self, instance):
        image_urls = []
        images_list = ProductImageSerializer(instance.product_img.all(), many=True,
                                             context={'request': self.context['request']}).data
        if len(images_list) > 0:
            for img in images_list:
                image_urls.append(img['image'])
        else:
            image_urls.append(
                'http://%s/media/default/placeholder.jpeg' % (self.context['request']).META.get('HTTP_HOST'))
        return image_urls

    class Meta:
        model = Product
        fields = (
            'id', 'pid', 'name', 'slug', 'unit', 'featured', 'hot_items', 'description',
            'sell_description', 'purchase_description', 'sell_price', 'offer_price', 'on_sale',
            'tags', 'attributes', 'status', 'super_sale', 'bmsm', 'images', 'category', 'subcategory',
            'created_at', 'updated_at'
        )
