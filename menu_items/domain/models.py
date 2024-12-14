import uuid
from django.db import models
from restaurants.domain.models import Restaurant

class MenuItem(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='menu_items')
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    preparation_time = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    category = models.CharField(max_length=100)
    image_url = models.CharField(max_length=255)
    

    def __str__(self):
        return self.name