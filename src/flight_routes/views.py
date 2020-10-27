from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.views import View
from passenger_view.models import ScheduledFlight
from .forms import ScheduledFlightForm, AirportForm


# Create your views here.
class AirportCreateView(View):
    """View for creating new airports"""

    def get(self, request, *args, **kwargs):
        form = AirportForm()

        if form.is_valid():
            form.save()
            form = AirportForm()
        context = {
            "form" : form
        }

        return render(request, "airport_create.html", context)

    def post(self, request, *args, **kwargs):
        form = AirportForm(request.POST)

        if form.is_valid():
            form.save()
            form = AirportForm()
        context = {
            "form": form
        }

        return HttpResponseRedirect(reverse("flight_routes:flight_routes_view"))

class FlightRoutesView(View):
    """View for seeing flight routes"""

    def get(self, request, *args, **kwargs):
        flight_routes = ScheduledFlight.objects.values_list(
            "origin_airport__airport_name",
            "origin_airport__airport_city",
            "origin_airport__airport_country",
            "destination_airport__airport_name",
            "destination_airport__airport_city",
            "destination_airport__airport_country",
            )
        context = {
            "flight_routes": flight_routes
        }
        return render(request, "flight_routes.html", context)


class ScheduledFlightCreateView(View):
    """View for creating new scheduled flight"""

    def get(self, request, *args, **kwargs):
        form = ScheduledFlightForm()

        if form.is_valid():
            form.save()
            form = ScheduledFlightForm()
        context = {
            "form" : form
        }
        return render(request, "scheduled_flight_create.html", context)

    def post(self, request, *args, **kwargs):
        form = ScheduledFlightForm(request.POST)
        if form.is_valid():
            form.save()
            form = ScheduledFlightForm()
        context = {
            "form": form
        }

        return HttpResponseRedirect(reverse("flight_routes:flight_routes_view"))
