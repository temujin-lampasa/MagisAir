from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse_lazy
from django.views import View
from passenger_view.models import (
    Crew,
    ScheduledFlight,
    CrewAssignment,
)
from django.views.generic import DetailView, CreateView
from .queries import QueryList


class HomeView(View):
    template_name = 'crew_assignments/home_view.html'

    def get(self, request, *args, **kwargs):
        crew_list = Crew.objects.all()
        flight_list = ScheduledFlight.objects.all()
        context = {'crew_list': crew_list, 'flight_list': flight_list}
        return render(request, self.template_name, context)


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
        # Get list of crew member assigned to the flight.
        assigned_crew = QueryList.assigned_crew_query(self.kwargs.get('flight_id'))
        context['assigned_crew'] = assigned_crew
        # Get list of passengers assigned to the flight
        passenger_list = QueryList.passenger_list_query(self.kwargs.get('flight_id'))
        context['passenger_list'] = passenger_list
        return context


class CrewAssignView(View):
    template_name = 'crew_assignments/crew_assign.html'
    checkbox_name = 'selected_flight_id'

    def get(self, request, *args, **kwargs):
        flights = ScheduledFlight.objects.all()
        context = {'flight_list': flights}
        request.session['last_crew_id'] = self.kwargs.get('crew_id')
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        selected_flight_IDs = request.POST.getlist(self.checkbox_name)
        # Perform a query to assign to selected flights.
        # If it hasn't already been added.
        last_crew_ID = request.session.get('last_crew_id')
        for flight_ID in selected_flight_IDs:
            try:
                QueryList.crew_assign_query(last_crew_ID, flight_ID)
            except:
                pass
        return HttpResponseRedirect(
            reverse_lazy('crew_assignments:crew_detail', args=(last_crew_ID,))
        )


class CrewCreateView(CreateView):
    model = Crew
    template_name = 'crew_assignments/crew_create.html'
    success_url = reverse_lazy("crew_assignments:crew_home")
    fields = ['crew_fname', 'crew_lname', 'crew_role']
    labels = {
        'crew_fname': 'First Name',
        'crew_lname': 'Last Name',
        'crew_role': 'Role'
    }
