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
        self.flights = QueryList.flight_select_query(
            flight_dep_date,
            origin_city,
            destination_city
        )
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
                request.session['total_cost'] = round(total_cost, 2)
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
            # Get the addons that have nonzero quantities and save to session.
            # Addon format = (id, description, cost, quantity)
            addon_quantities = list(form.cleaned_data.values())

            addons = models.Addon.objects.all()

            nonzero_addons = []
            additional_cost = 0  # total cost of additional addons
            for addon, qty in zip(addons, addon_quantities):
                if qty != '0':
                    r = (
                        addon.addon_id,
                        addon.addon_description,
                        addon.addon_cost,
                        qty
                    )
                    nonzero_addons.append(r)
                    additional_cost += int(addon.addon_cost) * int(qty)

            # Update the total cost session variable
            # by recalculating based on flight costs
            flight_cost = sum([f[-1] for f in request.session.get('flight_list', [0])])
            request.session['total_cost'] = flight_cost + additional_cost
            request.session['total_cost'] = round(request.session['total_cost'], 2)
            request.session['booking_addons'] = nonzero_addons

        return super().post(request, *args, **kwargs)


class ConfirmView(View):
    """View to confirm booking."""
    template_name = 'passenger_view/confirm_booking.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        # Save the data
        # INSERT in this order:
        # 1. Passenger
        # 2. Booking
        # 3. Booking_Addon_Map
        # 4. Itinerary

        REQUIRED_FIELDS = [
            'pass_fname', 'pass_lname', 'pass_mi', 'pass_bday', 'pass_gender',
            'booking_date', 'flight_list'
            ]

        missing_field = False
        for field in REQUIRED_FIELDS:
            if field not in request.session:
                missing_field = True
                break

        # TODO: rewrite to 'if missing_field'
        if not missing_field:
            # Insert a passenger
            pass_fname = request.session['pass_fname']
            pass_lname = request.session['pass_lname']
            pass_mi = request.session['pass_mi']
            pass_bday = request.session['pass_bday']
            pass_gender = request.session['pass_gender']
            # Get pass_id for later
            pass_id = QueryList.passenger_insert_query(
                pass_fname, pass_lname, pass_mi, pass_bday, pass_gender
            )

            # Insert a booking
            # get booking_id
            booking_id = QueryList.booking_insert_query(
                request.session['booking_date'], pass_id
            )

            # Booking Addon Map
            # Get the selected addons, if any
            try:
                addon_ids = [a[0] for a in request.session['booking_addons']]
                addon_quantities = [
                    a[-1] for a in request.session['booking_addons']
                ]
                QueryList.booking_addon_map_query(
                    booking_id, addon_ids, addon_quantities
                )
            except:
                pass

            # Itinerary / Booking-Flight Map
            flight_codes = [f[0] for f in request.session['flight_list']]
            flight_dep_dates = [f[3] for f in request.session['flight_list']]
            QueryList.itinerary_insert_query(
                booking_id, flight_codes, flight_dep_dates
            )
            print("DONE")

        context = {}
        return render(request, self.template_name, context)
