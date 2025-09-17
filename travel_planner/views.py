from django.views.generic import TemplateView, ListView, View
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Packages
from django.core.mail import send_mail
from django.conf import settings
from .forms import BookingForm
from django.urls import reverse
from .models import Booking

STATE_COORDS = {
    "Abia": [5.5320, 7.4860],
    "Adamawa": [9.3265, 12.3984],
    "Akwa Ibom": [4.9057, 7.8537],
    "Anambra": [6.2107, 7.0730],
    "Bauchi": [10.3158, 9.8442],
    "Bayelsa": [4.7719, 6.0699],
    "Benue": [7.1907, 8.1297],
    "Borno": [11.8333, 13.1500],
    "Cross River": [5.9631, 8.3268],
    "Delta": [5.5320, 5.8987],
    "Ebonyi": [6.3249, 8.1137],
    "Edo": [6.6342, 5.9304],
    "Ekiti": [7.6656, 5.3103],
    "Enugu": [6.4490, 7.5139],
    "Federal Capital Territory": [9.0765, 7.3986],
    "Gombe": [10.2899, 11.1670],
    "Imo": [5.5720, 7.0580],
    "Jigawa": [12.2280, 9.5616],
    "Kaduna": [10.5236, 7.4381],
    "Kano": [12.0022, 8.5919],
    "Katsina": [12.9880, 7.6223],
    "Kebbi": [12.4539, 4.1975],
    "Kogi": [7.7330, 6.6906],
    "Kwara": [8.9669, 4.3874],
    "Lagos": [6.5244, 3.3792],
    "Nasarawa": [8.5705, 8.3220],
    "Niger": [9.0810, 6.0176],
    "Ogun": [6.9980, 3.4737],
    "Ondo": [7.2508, 5.2103],
    "Osun": [7.5629, 4.5200],
    "Oyo": [7.3775, 3.9470],
    "Plateau": [9.2182, 9.5170],
    "Rivers": [4.8156, 7.0498],
    "Sokoto": [13.0667, 5.2339],
    "Taraba": [8.8870, 11.3700],
    "Yobe": [12.2939, 11.4397],
    "Zamfara": [12.1700, 6.6599],
}


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'travel_planner/home.html'


class PackagesView(LoginRequiredMixin, ListView):
    model = Packages
    template_name = 'travel_planner/packages.html'
    context_object_name = 'packages'

def map_view(request):
    user_coords = None
    dest_coords = None
    dest_name = None

    if request.method == "POST":
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)

            user_state = booking.address
            dest_state = booking.destination

            user_coords = STATE_COORDS.get(user_state)
            dest_coords = STATE_COORDS.get(dest_state)
            dest_name = dest_state

            if "show_map" in request.POST:
                messages.info(request, "Map preview updated. Confirm to save booking.")

            elif "confirm" in request.POST:
                booking.user = request.user
                booking.save()

                # Build approval/reject URLs
                approve_url = request.build_absolute_uri(
                    reverse("approve_booking", args=[booking.approval_token])
                )
                reject_url = request.build_absolute_uri(
                    reverse("reject_booking", args=[booking.approval_token])
                )

                # Send email to host
                send_mail(
                    subject="New Booking Request - Approval Needed",
                    message=(
                        f"A new booking has been submitted by {request.user}.\n\n"
                        f"Destination: {dest_state}\n"
                        f"Approve: {approve_url}\n"
                        f"Reject: {reject_url}\n"
                    ),
                    from_email="noreply@gmail.com",
                    recipient_list=["ad123eg456@gmail.com"],
                )

                messages.success(request, "Booking submitted! Awaiting host approval.")
    else:
        form = BookingForm()

    context = {
        "form": form,
        "user_coords": user_coords,
        "dest_coords": dest_coords,
        "dest_name": dest_name,
    }
    return render(request, "travel_planner/map.html", context)



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

def approve_booking(request, token):
    booking = get_object_or_404(Booking, approval_token=token)
    booking.status = "approved"
    booking.save()

    # Notify user
    send_mail(
        subject="Your Booking is Approved 🎉",
        message=f"Hi {booking.user.username}, your booking to {booking.destination} has been approved.",
        from_email="ad123eg456@gmail.com",
        recipient_list=[booking.user.email],
    )

    messages.success(request, "Booking approved and user notified.")
    return redirect("map_view")

def reject_booking(request, token):
    booking = get_object_or_404(Booking, approval_token=token)
    booking.status = "rejected"
    booking.save()

    # Notify user
    send_mail(
        subject="Your Booking was Rejected ❌",
        message=f"Hi {booking.user.username}, unfortunately your booking to {booking.destination} was rejected.",
        from_email="ad123eg456@gmail.com",
        recipient_list=[booking.user.email],
    )

    messages.warning(request, "Booking rejected and user notified.")
    return redirect("map_view")
