import uuid
from django.db import models
from django.conf import settings

class Booking(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    email = models.EmailField(null=True)
    address = models.CharField(max_length=255)
    destination = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    approval_token = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)

    def __str__(self):
        return f"{self.user} → {self.destination} ({self.status})"


class Packages(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=65)
    image = models.ImageField(upload_to='package_images/')