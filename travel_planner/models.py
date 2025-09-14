from django.db import models
from django.contrib.auth.models import User

class Booking(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    guests = models.PositiveIntegerField()
    arrival = models.DateField()
    leaving = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)

class Packages(models.Model):
    title = models.CharField(max_length=25)
    description = models.CharField(max_length=65)
    image = models.ImageField(upload_to='package_images/')