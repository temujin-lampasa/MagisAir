from django.shortcuts import render
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect
from django.views import View
from django.views.generic.edit import FormView

from .queries import QueryList
from .forms import (
    FlightSearchForm,
    PassengerInfoForm,
                    )


# Create your views here.
def home_view(request, *args, **kwargs):
    form = FlightSearchForm(request.POST or None)
    if form.is_valid():
        request.session['flight_dep_date'] = form.cleaned_data.get('date').strftime('%Y-%m-%d')
        request.session['from_city'] = form.cleaned_data.get('from_city')
        request.session['to_city'] = form.cleaned_data.get('to_city')
        return HttpResponseRedirect(reverse_lazy('passenger_view:pass_flights'))
    context = {'form': form}
    return render(request, 'passenger_view/home_view.html', context)


class FlightSelectView(View):
    template_name = 'passenger_view/flight_select.html'
    checkbox_name = 'flight_choice'

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
        flight_choice = request.POST.getlist(self.checkbox_name)
        if len(flight_choice) != 1:
            context['invalid_choice'] = True
            return render(request, self.template_name, context)
        else:
            context['invalid_choice'] = False
            request.session['chosen_flight'] = flight_choice[0]
            return HttpResponseRedirect(reverse_lazy('passenger_view:pass_info'))


def pass_info_view(request, *args, **kwargs):
    form = PassengerInfoForm(request.POST or None)

    if form.is_valid():
        return HttpResponseRedirect(reverse_lazy('passenger_view:addon_select'))

    context = {"form": form}
    return render(request, 'passenger_view/pass_info.html', context)


class PassInfoView(FormView):
    template_name = 'passenger_view/pass_info.html'
    form_class = PassengerInfoForm
    success_url = reverse_lazy('passenger_view:addon_select')


class AddonSelectView(View):
    template_name = 'passenger_view/addon_select.html'

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)
