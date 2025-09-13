from django.contrib import admin
from .models import Category, Service, Order, Review, Notification
admin.site.register(Category); 
admin.site.register(Service); 
admin.site.register(Order); 
admin.site.register(Review); 
admin.site.register(Notification)
