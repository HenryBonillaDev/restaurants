from django.db import models
import uuid


class Restaurant(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2, null=True, blank=True)
    status = models.CharField(max_length=20)
    category = models.CharField(max_length=100, null=True, blank=True)
    latitude = models.DecimalField(
        max_digits=21, decimal_places=11, null=True, blank=True
    )
    longitude = models.DecimalField(
        max_digits=21, decimal_places=11, null=True, blank=True
    )

    def __str__(self):
        return self.name
