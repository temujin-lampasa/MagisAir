from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView
import passenger_view.models as models
from .queries import QueryList
import datetime
from .forms import (
    FlightSearchForm,
    PassengerInfoForm,
    AddonSelectForm
                    )


# Create your views here.
class HomeView(View):
    """View for finding flight, with form for departure date
    and origin/destination cities."""
    template_name = 'passenger_view/home_view.html'

    def get(self, request, *args, **kwargs):
        form = FlightSearchForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            # Save selected cities and departure date to session
            request.session['flight_dep_date'] = form.cleaned_data.get('date').strftime('%Y-%m-%d')
            request.session['from_city'] = form.cleaned_data.get('from_city')
            request.session['to_city'] = form.cleaned_data.get('to_city')
            request.session['booking_date'] = datetime.date.today().strftime('%Y-%m-%d')
            return HttpResponseRedirect(reverse_lazy('passenger_view:pass_flights'))
        context = {'form': form}
        return render(request, self.template_name, context)


class FlightSelectView(View):
    """View for selecting a flight with matching date and cities
    given by HomeView."""
    template_name = 'passenger_view/flight_select.html'
    checkbox_name = 'flight_code'

    def dispatch(self, request, *args, **kwargs):
        # Get cities and date from session
        # Then use to query flights with matching info
        flight_dep_date = request.session.get('flight_dep_date')
        origin_city = request.session.get('from_city')
        destination_city = request.session.get('to_city')
        self.flights = QueryList.flight_select_query(flight_dep_date,
                                                     origin_city,
                                                     destination_city)
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        context = {'object_list': self.flights}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Instantiate session flight_list
        if 'flight_list' not in request.session:
            request.session['flight_list'] = []
        # Validate the form data.
        # Make sure only 1 checkbox selected.
        context = {'object_list': self.flights}
        chosen_flight_code = request.POST.getlist(self.checkbox_name)
        if len(chosen_flight_code) != 1:
            context['invalid_choice'] = True
            return render(request, self.template_name, context)
        else:
            context['invalid_choice'] = False
            # The choice is valid
            # Find out which flight was chosen,
            # then add the flight to the session flight_list
            chosen_flight = None
            for flight in self.flights:
                if flight.flight_code == chosen_flight_code[0]:
                    chosen_flight = flight

            # Check if the chosen flight isn't already added.
            if (chosen_flight.flight_code not in
               [f[0] for f in request.session['flight_list']]):
                # Turn the FlightRow into something JSON serializable
                request_content = [
                    chosen_flight.flight_code,
                    chosen_flight.airport_origin,
                    chosen_flight.airport_destination,
                    chosen_flight.flight_dep_date,
                    chosen_flight.flight_arrival_date,
                    str(chosen_flight.flight_duration),
                    chosen_flight.flight_cost,
                    ]
                # Save to session
                # Can't append directly to session list
                # Must be done this way
                session_flight_list = request.session['flight_list']
                session_flight_list.append(request_content)
                request.session['flight_list'] = session_flight_list

                # Then calculate and save the total cost of those flights
                total_cost = sum([i[-1] for i in session_flight_list])
                request.session['total_cost'] = total_cost
            return HttpResponseRedirect(reverse_lazy('passenger_view:pass_info'))


class PassInfoView(FormView):
    """View for entering passenger information."""
    template_name = 'passenger_view/pass_info.html'
    form_class = PassengerInfoForm
    success_url = reverse_lazy('passenger_view:addon_select')

    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Save passenger info to session.
            request.session['pass_fname'] = form.cleaned_data.get('pass_fname')
            request.session['pass_lname'] = form.cleaned_data.get('pass_lname')
            request.session['pass_mi'] = form.cleaned_data.get('pass_mi')
            request.session['pass_bday'] = form.cleaned_data.get('pass_bday').strftime('%Y-%m-%d')
            request.session['pass_gender'] = form.cleaned_data.get('pass_gender')
        return super().post(request, *args, **kwargs)


class AddonSelectView(FormView):
    """View for selecting addons."""
    template_name = 'passenger_view/addon_select.html'
    form_class = AddonSelectForm
    success_url = reverse_lazy('passenger_view:confirmation_view')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            # Save the quantities of the addons to session
            addon_quantities = list(form.cleaned_data.values())
            request.session['addon_quantities'] = addon_quantities

            # addon_booking_display is only for use in the booking_summary.
            # Show only addons whose quantity is not 0
            addons = [a.addon_description for a in models.Addon.objects.all()]
            nonzero_addons = [
                a for a, b in zip(addons, addon_quantities) if b != '0'
            ]
            nonzero_quantities = [a for a in addon_quantities if a != '0']
            addon_booking_display = list(zip(nonzero_addons, nonzero_quantities))
            request.session['addon_booking_display'] = addon_booking_display
        return super().post(request, *args, **kwargs)


class ConfirmView(View):
    """View to confirm booking."""
    template_name = 'passenger_view/confirm_booking.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # TODO
        context = {}
        return render(request, self.template_name, context)
