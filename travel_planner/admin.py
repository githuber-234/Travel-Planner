from django.contrib import admin
from .models import Booking, Packages


@admin.register(Booking)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'address', 'destination')
    
@admin.register(Packages)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'image')

