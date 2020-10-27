from django.urls import path
from .views import (
    FlightRoutesView,
    ScheduledFlightCreateView,
    AirportCreateView
)

app_name = "flight_routes"
urlpatterns = [
    path('', FlightRoutesView.as_view(), name='flight_routes_view'),
    path('scheduled_flight_create/', ScheduledFlightCreateView.as_view(), name='scheduled_flight_create'),
    path('airport_create/', AirportCreateView.as_view(), name='airport_create'),
]
