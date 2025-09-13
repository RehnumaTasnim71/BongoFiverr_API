from rest_framework import viewsets, generics, filters
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Service, Order, Review, Notification
from .serializers import (
    CategorySerializer,
    ServiceSerializer,
    OrderSerializer,
    ReviewSerializer,
    NotificationSerializer, 
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.exceptions import PermissionDenied
from rest_framework import viewsets, permissions


# --- Services ---
class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(active=True)
    serializer_class = ServiceSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    filter_backends = [DjangoFilterBackend, filters.OrderingFilter, filters.SearchFilter]
    filterset_fields = ["category"] 
    ordering_fields = ["price", "created_at"] 
    search_fields = ["title", "description"] 


# --- Orders ---
class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        if user.is_seller():
            return Order.objects.filter(seller=user)  
        return Order.objects.filter(buyer=user) 

    def perform_create(self, serializer):
        serializer.save(buyer=self.request.user)


# --- Reviews ---
class ReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        order = serializer.validated_data["order"]
        if order.buyer != self.request.user:
            raise PermissionDenied("You can only review your own orders.")
        if order.status != "completed":
            raise PermissionDenied("You can only review completed orders.")
        serializer.save(reviewer=self.request.user)


class ReviewsByServiceView(generics.ListAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        service_id = self.kwargs["service_id"]
        return Review.objects.filter(order__service_id=service_id)


# --- Notifications ---
class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(user=self.request.user).order_by("-created_at")

class SellerServiceViewSet(viewsets.ModelViewSet):
    serializer_class = ServiceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Service.objects.filter(seller=self.request.user)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)

# Place an order
class PlaceOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, service_id):
        try:
            service = Service.objects.get(id=service_id, active=True)
        except Service.DoesNotExist:
            return Response(
                {"detail": "Service not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "service": service.id,
            "buyer": request.user.id,
            "seller": service.seller.id,
            "price": service.price,
            "instructions": request.data.get("instructions", "")
        }

        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        order = serializer.save()

        Notification.objects.create(
            user=service.seller,
            title="New Order Placed",
            message=f"You have a new order from {request.user.username} for '{service.title}'."
        )
        Notification.objects.create(
            user=request.user,
            title="Order Placed",
            message=f"Your order for '{service.title}' has been placed successfully."
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
# Buyer order history
class BuyerOrderHistoryView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(buyer=self.request.user).order_by('-created_at')