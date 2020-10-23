from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView
import passenger_view.models as models

from .queries import QueryList
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
            request.session['flight_code'] = None
            return HttpResponseRedirect(reverse_lazy('passenger_view:pass_flights'))
        context = {'form': form}
        return render(request, self.template_name, context)


class FlightSelectView(View):
    """View for selecting a flight with matching date and cities
    given by HomeView."""
    template_name = 'passenger_view/flight_select.html'
    checkbox_name = 'flight_choice'

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
        # Validate the form data.
        # Make sure only 1 checkbox selected.
        context = {'object_list': self.flights}
        flight_choice = request.POST.getlist(self.checkbox_name)
        if len(flight_choice) != 1:
            context['invalid_choice'] = True
            return render(request, self.template_name, context)
        else:
            context['invalid_choice'] = False
            request.session['flight_code'] = flight_choice[0]
            return HttpResponseRedirect(reverse_lazy('passenger_view:pass_info'))


class PassInfoView(FormView):
    """View for entering passenger information."""
    template_name = 'passenger_view/pass_info.html'
    form_class = PassengerInfoForm
    success_url = reverse_lazy('passenger_view:addon_select')

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
            # Save fields to session
            pass
        return super().post(request, *args, **kwargs)


class ConfirmationView(View):
    """View to confirm booking."""
    template_name = 'passenger_view/confirm_booking.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # TODO
        context = {}
        return render(request, self.template_name, context)
