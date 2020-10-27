from django.urls import path
from .views import (
    HomeView,
    CrewDetailView,
    FlightDetailView,
    CrewAssignView,
)

app_name = 'crew_assignments'
urlpatterns = [
    path('', HomeView.as_view(), name='crew_home'),
    path('crew/<int:crew_id>', CrewDetailView.as_view(), name='crew_detail'),
    path('flight/<int:flight_id>', FlightDetailView.as_view(), name='flight_detail'),
    path('crew/assign/<int:crew_id>', CrewAssignView.as_view(), name='crew_assign')
]
