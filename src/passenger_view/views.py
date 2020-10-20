from django.shortcuts import render, reverse
from .forms import FlightSearchForm
from django.http import HttpResponseRedirect
from django.db import connection

from .queries import QueryList


# Create your views here.
def home_view(request, *args, **kwargs):
    form = FlightSearchForm(request.POST or None)
    print(request.session)
    if form.is_valid():
        print(form.cleaned_data)
        request.session['flight_dep_date'] = form.cleaned_data.get('date').strftime('%Y-%m-%d')
        return HttpResponseRedirect(reverse('passenger_view:pass_flights'))
    context = {'form': form}
    return render(request, 'passenger_view/home_view.html', context)


def flight_select_view(request, *args, **kwargs):
    flight_dep_date = request.session.get('flight_dep_date')
    flights = QueryList.flight_dep_date_query(flight_dep_date)
    context = {'object_list': flights}
    return render(request, 'passenger_view/flight_select.html', context)
