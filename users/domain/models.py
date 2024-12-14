import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from restaurants.domain.models import Restaurant

class User(AbstractUser):
    DEALER = 'dealer'
    CUSTOMER = 'customer'
    ROLE_CHOICES = [
        (DEALER, 'Dealer'),
        (CUSTOMER, 'Customer'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    restaurant = models.ForeignKey(
        Restaurant,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='users'
    )
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=255, unique=True)
    phone = models.CharField(max_length=20)
    default_address = models.TextField()

    groups = models.ManyToManyField( 'auth.Group', related_name='custom_user_set' )
    user_permissions = models.ManyToManyField( 'auth.Permission', related_name='custom_user_set' )

    def __str__(self):
        return self.username