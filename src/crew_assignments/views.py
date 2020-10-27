from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.views import View
from passenger_view.models import (
    Crew,
    ScheduledFlight,
    CrewAssignment
)
from django.views.generic import DetailView
from .queries import QueryList


def index(request):
    return HttpResponse("Hello, world. You're at the crew assignments index.")


class HomeView(View):
    template_name = 'crew_assignments/home_view.html'
    crew_list = Crew.objects.all()
    flight_list = ScheduledFlight.objects.all()
    context = {'crew_list': crew_list, 'flight_list': flight_list}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)


class CrewDetailView(DetailView):
    model = Crew
    template_name = 'crew_assignments/crew_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("crew_id")
        return get_object_or_404(Crew, crew_id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assigned_flights = QueryList.assigned_flights_query(self.kwargs.get("crew_id"))
        context['assigned_flights'] = assigned_flights
        return context


class FlightDetailView(DetailView):
    model = ScheduledFlight
    template_name = 'crew_assignments/flight_detail.html'

    def get_object(self):
        id_ = self.kwargs.get("flight_id")
        return get_object_or_404(ScheduledFlight, flight_id=id_)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        assigned_crew = QueryList.assigned_crew_query(self.kwargs.get("flight_id"))
        context['assigned_crew'] = assigned_crew
        return context
