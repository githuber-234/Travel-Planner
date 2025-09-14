from django.views.generic import TemplateView, CreateView, ListView, View
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Booking, Packages
from django.core.mail import send_mail
from django.conf import settings


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'travel_planner/home.html'


class PackagesView(LoginRequiredMixin, ListView):
    model = Packages
    template_name = 'travel_planner/packages.html'
    context_object_name = 'packages'

class BookView(LoginRequiredMixin, CreateView, ListView):
    model = Booking
    fields = ["phone", "address", "location", "guests", "arrival", "leaving"]  
    template_name = "travel_planner/book.html"
    success_url = reverse_lazy("book")
    context_object_name = "bookings"

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.name = self.request.user.first_name or self.request.user.username
        form.instance.email = self.request.user.email

        response = super().form_valid(form)

        booking = form.instance  # the saved booking object

        # Build message with all booking details
        message_body = (
            f"Hello {booking.name},\n\n"
            f"Your booking has been received successfully with the following details:\n\n"
            f"Name: {booking.name}\n"
            f"Email: {booking.email}\n"
            f"Phone: {booking.phone}\n"
            f"Address: {booking.address}\n"
            f"Location: {booking.location}\n"
            f"Guests: {booking.guests}\n"
            f"Arrival Date: {booking.arrival}\n"
            f"Leaving Date: {booking.leaving}\n\n"
            "We will contact you soon with more information.\n\n"
            "Thank you for choosing us!"
        )

        # Send confirmation email
        send_mail(
            subject="Booking Confirmation",
            message=message_body,
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[booking.email],
            fail_silently=False,
        )

        messages.success(
            self.request,
            "Your booking was submitted successfully! A confirmation email with your details has been sent to you."
        )
        return response

    def get_queryset(self):
        return Booking.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["packages"] = Packages.objects.all()
        return context

class ContactView(LoginRequiredMixin, View):
    template_name = 'travel_planner/contact.html'
    success_url = '/contact/'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '')
        email = request.POST.get('email', '')
        message = request.POST.get('message', '')

        if name and email and message:
            send_mail(
                "Travel Itinerary - Contact",
                f"From: {name} <{email}>\n\nMessage:\n{message}",
                settings.DEFAULT_FROM_EMAIL,
                ['ad123eg456@gmail.com'],
            )
            return redirect(self.success_url)

        return render(request, self.template_name, {
            'error': "All fields are required.",
            'form_data': {'name': name, 'email': email, 'message': message}
        })
