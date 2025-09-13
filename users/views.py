from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import MyTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer, UserSerializer, ProfileUpdateSerializer
from .tokens import account_activation_token
from market.models import Service, Order, Review
from rest_framework.views import APIView
from rest_framework import generics, permissions
from . import models

User = get_user_model()

# Registration with email activation
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        link = self.request.build_absolute_uri(
            reverse('users:activate', kwargs={'uidb64': uid, 'token': token})
        )
        send_mail('Activate your account', f'Activate: {link}', 'no-reply@example.com', [user.email])

# Account activation
class ActivateView(generics.GenericAPIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({'detail':'Invalid activation link.'}, status=status.HTTP_400_BAD_REQUEST)

        if account_activation_token.check_token(user, token):
            user.email_verified = True
            user.save()
            return Response({'detail':'Account activated.'})
        return Response({'detail':'Invalid token.'}, status=status.HTTP_400_BAD_REQUEST)

# Current user info
class MeView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# JWT Login
class LoginView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

class LoginView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


# -----------------------------
# Seller Dashboard
# -----------------------------
class SellerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_seller():
            return Response({"detail": "Only sellers can access this."}, status=403)

        services = Service.objects.filter(seller=request.user)
        orders = Order.objects.filter(service__in=services)
        reviews = Review.objects.filter(order__service__in=services)
        earnings = orders.filter(status='completed').aggregate(total=models.Sum('price'))['total'] or 0

        return Response({
            "services": [{"id": s.id, "title": s.title, "price": s.price, "active": s.active} for s in services],
            "orders": [{"id": o.id, "service": o.service.title, "buyer": o.buyer.username, "status": o.status} for o in orders],
            "reviews": [{"service": r.order.service.title, "rating": r.rating, "comment": r.comment} for r in reviews],
            "earnings": earnings
        })

# -----------------------------
# Buyer Dashboard
# -----------------------------
class BuyerDashboardView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if not request.user.is_buyer():
            return Response({"detail": "Only buyers can access this."}, status=403)

        orders = Order.objects.filter(buyer=request.user)
        reviews = Review.objects.filter(order__buyer=request.user)

        return Response({
            "orders": [{"id": o.id, "service": o.service.title, "seller": o.seller.username, "status": o.status} for o in orders],
            "reviews": [{"service": r.order.service.title, "rating": r.rating, "comment": r.comment} for r in reviews]
        })
    

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user