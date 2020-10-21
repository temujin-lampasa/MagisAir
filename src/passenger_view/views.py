from django.shortcuts import render, reverse
from .forms import FlightSearchForm
from django.http import HttpResponseRedirect
from django.db import connection

from .queries import QueryList


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


def flight_select_view(request, *args, **kwargs):
    flight_dep_date = request.session.get('flight_dep_date')
    origin_city = request.session.get('from_city')
    destination_city = request.session.get('to_city')
    flights = QueryList.flight_select_query(flight_dep_date,
                                            origin_city,
                                            destination_city)
    context = {'object_list': flights}
    return render(request, 'passenger_view/flight_select.html', context)
