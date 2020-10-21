from django.shortcuts import render, reverse
from django.http import HttpResponseRedirect
from django.db import connection
from django.views import View

from .queries import QueryList
from .forms import (
    FlightSearchForm,
    PassengerInfoForm
                    )


# Create your views here.
def home_view(request, *args, **kwargs):
    form = FlightSearchForm(request.POST or None)
    if form.is_valid():
        request.session['flight_dep_date'] = form.cleaned_data.get('date').strftime('%Y-%m-%d')
        request.session['from_city'] = form.cleaned_data.get('from_city')[0]
        request.session['to_city'] = form.cleaned_data.get('to_city')[0]
        return HttpResponseRedirect(reverse('passenger_view:pass_flights'))
    context = {'form': form}
    return render(request, 'passenger_view/home_view.html', context)


# def flight_select_view(request, *args, **kwargs):
#
#     # Validate
#     checkbox_name = 'flight_choice'
#     print(f"POST list: {request.POST.getlist(checkbox_name)}")
#
#     flight_dep_date = request.session.get('flight_dep_date')
#     origin_city = request.session.get('from_city')
#     destination_city = request.session.get('to_city')
#     flights = QueryList.flight_select_query(flight_dep_date,
#                                             origin_city,
#                                             destination_city)
#     context = {'object_list': flights}
#     return render(request, 'passenger_view/flight_select.html', context)


class FlightSelectView(View):
    template_name = 'passenger_view/flight_select.html'

    def dispatch(self, request, *args, **kwargs):
        # Set variables to be used:
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
        context = {'object_list': self.flights}
        return render(request, self.template_name, context)


def pass_info_view(request, *args, **kwargs):
    form = PassengerInfoForm(request.POST or None)

    context = {"form": form}
    return render(request, 'passenger_view/pass_info.html', context)
