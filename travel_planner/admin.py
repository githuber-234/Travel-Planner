from django.contrib import admin
from .models import Booking, Packages


@admin.register(Booking)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'phone', 'address',
                    'location', 'guests', 'arrival', 'leaving')
    
@admin.register(Packages)
class AssessmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'image')

