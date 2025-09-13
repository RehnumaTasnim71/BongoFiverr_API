from rest_framework import serializers
from .models import Category, Service, Order, Review, Notification
from django.contrib.auth import get_user_model
User = get_user_model()

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id','name','slug']

class ServiceSerializer(serializers.ModelSerializer):
    seller = serializers.ReadOnlyField(source='seller.username')
    class Meta:
        model = Service
        fields = ['id','title','slug','description','price','delivery_days','category','seller','active','created_at']

class OrderSerializer(serializers.ModelSerializer):
    buyer = serializers.ReadOnlyField(source='buyer.username')
    seller = serializers.ReadOnlyField(source='seller.username')
    class Meta:
        model = Order
        fields = ['id','buyer','seller','service','instructions','status','price','created_at','delivered_at']

class ReviewSerializer(serializers.ModelSerializer):
    reviewer = serializers.ReadOnlyField(source='reviewer.username')
    class Meta:
        model = Review
        fields = ['id','order','reviewer','rating','comment','created_at']

class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = ['id','title','message','read','created_at']

class OrderSerializer(serializers.ModelSerializer):
    service_title = serializers.CharField(source='service.title', read_only=True)
    seller_username = serializers.CharField(source='seller.username', read_only=True)

    class Meta:
        model = Order
        fields = [
            'id', 'service', 'service_title', 'seller', 'seller_username',
            'buyer', 'instructions', 'status', 'created_at', 'delivered_at', 'price'
        ]
        read_only_fields = ['id', 'buyer', 'seller', 'status', 'created_at', 'delivered_at', 'price']