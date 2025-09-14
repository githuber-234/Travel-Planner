from django.urls import path
from .views import (HomeView, PackagesView, BookView, ContactView)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('packages/', PackagesView.as_view(), name='packages'),
    path('book/', BookView.as_view(), name='book'),
    path('contact/', ContactView.as_view(), name='contact'),
]