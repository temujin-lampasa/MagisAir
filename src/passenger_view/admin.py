from django.contrib import admin

# Register your models here.
from passenger_view.models import (
    Addon,
    Airport,
    Booking,
    # BookingAddonMap,
    Crew,
    # CrewFlightMap,
    ScheduledFlight,
    Itinerary,
    Passenger,
)


models = (
    Addon,
    Airport,
    Booking,
    # BookingAddonMap,
    Crew,
    # CrewFlightMap,
    ScheduledFlight,
    Itinerary,
    Passenger,
)

for model in models:
    try:
        admin.site.register(model)
    except admin.sites.AlreadyRegistered:
        pass
