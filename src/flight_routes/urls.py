from django.urls import path
from .views import FlightRoutesView

urlpatterns = [
	path('', FlightRoutesView.as_view(), name='flight_routes_view'),
]
