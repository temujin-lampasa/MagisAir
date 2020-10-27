from django.shortcuts import render
from django.views import View
from itertools import permutations
from passenger_view.models import Airport, ScheduledFlight
from .forms import ScheduledFlightForm

# Create your views here.


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

        return render(request, "scheduled_flight_create.html", context)
