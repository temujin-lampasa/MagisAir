from django.urls import path
from .views import FlightRoutesView, ScheduledFlightCreateView

urlpatterns = [
	path('', FlightRoutesView.as_view(), name='flight_routes_view'),
	path('scheduled_flight_create/', ScheduledFlightCreateView.as_view(), name='scheduled_flight_create'),
]
