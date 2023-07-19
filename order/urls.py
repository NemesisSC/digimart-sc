from django.urls import path, include

from .views import *


urlpatterns = [
    path('my', orders),
    path('my/delivered', mydeliveredOrders),
    path('create', createOrder),
    path('details/<str:order_id>', orderDetails),
    path('list', ordersAdminList),
    path('list/pending', pendingOrders),
    path('list/approved', approvedOrders),
    path('list/rejected', rejectedOrders),
    
    path('list/delivery-pending', deliveryPendingOrders),
    path('list/delivered', deliveredOrders),
    
    
    path('edit-order-status/<int:pk>/<str:order_status>', EditOrderStatus),
    path('edit-delivery-status/<int:pk>/<str:delivery_status>', EditDeliveryStatus),
    
    path('count', count),
    
    
    
    
    
    # path('sub', get_sub_category),
    # path('new', categoryCreate),
    # path('edit/<int:category_id>', categoryEdit),
    # path('delete/<int:category_id>', categoryDelete),
    # path('featured/<int:category_id>', categoryFeatureToggle),
    # path('status/<int:category_id>', categoryStatusToggle),
    # path('by-parent', getCategoryByParent),
]