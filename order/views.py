from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import *
from .serializers import * 

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def createOrder(request):
    try:
        user = request.user
        cart_items = CartItem.objects.filter(cart__user=user)
        data = request.data

        if not cart_items.exists():
            return Response({'error': 'Cart is empty.'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.total_price() for item in cart_items)

        order = Order.objects.create(user=user, total_price=total_price, message = request.data['message'])

        for cart_item in cart_items:
            OrderItem.objects.create(order=order, product=cart_item.product, quantity=cart_item.quantity)
            
        product_ids = cart_items.values_list('product', flat=True)
        Product.objects.filter(id__in=product_ids).update(status=False)

        serializer = OrderSerializer(order)
        # Clear cart after successful order placement
        cart_items.delete()

        return Response({
            'code': status.HTTP_200_OK,
            'response': "Order Created Successfully",
            
        })
    
    except Exception as e:
        print(e)
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Errors in data",
            'error': str(e)
        })



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def orders(request):
    try:
        user = request.user
        orders = Order.objects.filter(user=user)
        serializer = OrderReadSerializer(orders, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })
        
@api_view(['GET'])
def orderDetails(request, order_id):
    try:
        order_details = Order.objects.get(id=order_id)
        print(order_details)
        product_serializer = OrderAdminSerializer(order_details, context={'request': request})
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Order Details Data Successfully",
            "data": product_serializer.data

        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def ordersAdminList(request):
    try:
        
        orders = Order.objects.all()
        serializer = OrderAdminSerializer(orders, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def pendingOrders(request):
    try:
        
        orders = Order.objects.filter(order_status = "PENDING")
        serializer = OrderAdminSerializer(orders, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def approvedOrders(request):
    try:
        
        orders = Order.objects.filter(order_status = "APPROVED")
        serializer = OrderAdminSerializer(orders, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def rejectedOrders(request):
    try:
        
        orders = Order.objects.filter(order_status = "REJECTED")
        serializer = OrderAdminSerializer(orders, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deliveryPendingOrders(request):
    try:
        
        orders = Order.objects.filter(delivery_status = "PENDING" ,order_status = "APPROVED")
        serializer = OrderAdminSerializer(orders, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def deliveredOrders(request):
    try:
        
        orders = Order.objects.filter(delivery_status = "DELIVERED" ,order_status = "APPROVED")
        serializer = OrderAdminSerializer(orders, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def mydeliveredOrders(request):
    try:
        user = request.user
        orders = Order.objects.filter(user = user, delivery_status = "DELIVERED" ,order_status = "APPROVED")
        serializer = OrderAdminSerializer(orders, many=True)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Received Data Successfully",
            "data": serializer.data
        })
    
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': e
        })
        
        
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def EditOrderStatus(request, pk, order_status):
    try:
        order = Order.objects.get(id=pk)
        order.order_status = order_status
        order.save()
        serializer = OrderSerializer(order)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Order Status Updated Successfully",
            'data': serializer.data

        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def EditDeliveryStatus(request, pk, delivery_status):
    try:
        order = Order.objects.get(id=pk)
        order.delivery_status = delivery_status
        order.save()
        serializer = OrderSerializer(order)
        return Response({
            'code': status.HTTP_200_OK,
            'response': "Order Delivery Status Updated Successfully",
            'data': serializer.data

        })

    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })
        
        
@api_view(['GET'])
def count(request):
    try:
        category_count = Category.objects.all().count()
        product_count = Product.objects.all().count()
        order_count = Order.objects.all().count()
        student_count = ProductUser.objects.all().count()

        return Response({
            'Response': 'Count received successfully',
            'Category': category_count,
            'Product': product_count,
            'Orders': order_count,
            'Student_Product': student_count,


        })
    except Exception as e:
        return Response({
            'code': status.HTTP_400_BAD_REQUEST,
            'response': "Data not found",
            'error': str(e)
        })