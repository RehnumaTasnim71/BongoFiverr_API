from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import PlaceOrderView, BuyerOrderHistoryView
from .views import (
    ServiceViewSet,
    OrderViewSet,
    ReviewCreateView,
    ReviewsByServiceView,
    NotificationListView, 
    PlaceOrderView,
    BuyerOrderHistoryView,
)

router = DefaultRouter()
router.register('services', ServiceViewSet, basename='services')
router.register('orders', OrderViewSet, basename='orders')

urlpatterns = [
    path('', include(router.urls)),

    # Reviews
    path('reviews/', ReviewCreateView.as_view(), name='review-create'),
    path('reviews/service/<int:service_id>/', ReviewsByServiceView.as_view(), name='reviews-by-service'),

    # Notifications
    path('notifications/', NotificationListView.as_view(), name='notifications'),

    path('orders/place/<int:service_id>/', PlaceOrderView.as_view(), name='place-order'),
    path('orders/my/', BuyerOrderHistoryView.as_view(), name='buyer-order-history'),
]
