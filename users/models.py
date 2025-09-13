from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    ROLE_CHOICES = (('buyer','Buyer'), 
                    ('seller','Seller'))
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    email_verified = models.BooleanField(default=False)
    def is_seller(self): 
        return self.role == 'seller'
    def is_buyer(self): 
        return self.role == 'buyer'
