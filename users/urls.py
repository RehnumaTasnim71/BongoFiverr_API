from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.urls import path
from .views import RegisterView, MeView, ActivateView, LoginView
from .views import SellerDashboardView, BuyerDashboardView, ProfileUpdateView

app_name = 'users'

@api_view(['GET'])
def users_root(request):
    return Response({
        "register": "register/",
        "login": "login/",
        "me": "me/",
        "activate": "activate/<uidb64>/<token>/"
    })

urlpatterns = [
    path('', users_root, name='users-root'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),   
    path('me/', MeView.as_view(), name='me'),
    path('activate/<uidb64>/<token>/', ActivateView.as_view(), name='activate'),
    path('seller-dashboard/', SellerDashboardView.as_view(), name='seller-dashboard'),
    path('buyer-dashboard/', BuyerDashboardView.as_view(), name='buyer-dashboard'),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
]
