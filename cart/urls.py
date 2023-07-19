from django.urls import path, include

from .views import *


urlpatterns = [
    path('', viewCart),
    path('item/list/<int:cart_id>', cartItems),
    path('item/create', addToCart),
    path('item/delete/<int:cartItem_id>', removeItemFromCart),
    
]