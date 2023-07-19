from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import * 



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def viewCart(request):
    try:
        try:
            cart = Cart.objects.get(user=request.user)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart does not exist.'}, status=400)

        serializer = CartReadSerializer(cart)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Retrieve Cart Successfully",
            "data": serializer.data
        })
    
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def addToCart(request):
    try:
        user = request.user
        if not user.is_authenticated:
            return Response({'error': 'User not authenticated'}, status=401)

        try:
            cart = Cart.objects.get(user=user)
        except Cart.DoesNotExist:
            cart = Cart.objects.create(user=user)

        product_id = request.data.get('product')
        quantity = request.data.get('quantity', 1)

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response({'error': 'Product not found'}, status=404)

        cart_item = CartItem(cart=cart, product=product, quantity=quantity)
        cart_item.save()

        serializer = CartItemSerializer(cart_item)
        
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Item added to Cart Successfully",
            "data": serializer.data
        })
        
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })

@api_view(['GET'])
def cartItems(request, cart_id):
    try:
        cart = Cart.objects.get(id=cart_id)
    

        cart_items = cart.cartitem_set.all()
        serializer = CartItemSerializer(cart_items, many=True)
        return Response(serializer.data)

    except Cart.DoesNotExist:
        return Response({'error': 'Cart not found'}, status=404)


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def removeItemFromCart(request, cartItem_id):
    try:
        item = CartItem.objects.get(id= cartItem_id)
        item.delete()
        return Response({'code': status.HTTP_200_OK,'response': 'Data Deleted'})
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })