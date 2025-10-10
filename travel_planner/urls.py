from django.urls import path
from .views import (HomeView, BookView, ContactView, BookingSuccessView, TripsView)
from . import views

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('book/', BookView.as_view(), name='book'),
    path('booking-success/', BookingSuccessView.as_view(), name='booking-success'),
    path('map/', views.map_view, name='map'),
    path('trips/', TripsView.as_view(), name='trips'),
    path('contact/', ContactView.as_view(), name='contact'),
    path("approve/<uuid:token>/", views.approve_booking, name="approve_booking"),
    path("reject/<uuid:token>/", views.reject_booking, name="reject_booking"),
    path('download-report/<int:booking_id>/', views.download_report, name='download_report'),
]