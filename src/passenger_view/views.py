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
    AddonSelectForm,
    AddonQuantityForm,
                    )


# Create your views here.
class HomeView(View):
    template_name = 'passenger_view/home_view.html'

    def get(self, request, *args, **kwargs):
        form = FlightSearchForm()
        context = {'form': form}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        form = FlightSearchForm(request.POST)
        if form.is_valid():
            request.session['flight_dep_date'] = form.cleaned_data.get('date').strftime('%Y-%m-%d')
            request.session['from_city'] = form.cleaned_data.get('from_city')
            request.session['to_city'] = form.cleaned_data.get('to_city')
            return HttpResponseRedirect(reverse_lazy('passenger_view:pass_flights'))
        context = {'form': form}
        return render(request, self.template_name, context)


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


class PassInfoView(FormView):
    template_name = 'passenger_view/pass_info.html'
    form_class = PassengerInfoForm
    success_url = reverse_lazy('passenger_view:addon_select')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            fn = form.cleaned_data.get('pass_fname')
            ln = form.cleaned_data.get('pass_lname')
            mn = form.cleaned_data.get('pass_mi')
            request.session['pass_fname'] = fn
            request.session['pass_lname'] = ln
            request.session['pass_mi'] = mn
            request.session['pass_name'] = f"{ln}, {fn} {mn}."
        return super().post(request, *args, **kwargs)


class AddonSelectView(FormView):
    template_name = 'passenger_view/addon_select.html'
    form_class = AddonSelectForm
    success_url = reverse_lazy('passenger_view:addon_qty_select')

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():
            selected_addon_ids = form.cleaned_data.get('addon_field')
            selected_addon_ids = tuple([int(id) for id in selected_addon_ids])
            selected_addons = models.Addon.objects.filter(addon_id__in=selected_addon_ids)
            selected_addons = [a.__str__() for a in selected_addons]
            print(selected_addons)
            request.session['addon_list'] = selected_addons
        return super().post(request, *args, **kwargs)


class AddonQuantityView(FormView):
    template_name = 'passenger_view/addon_qty_select.html'
    success_url = ""
    form_class = AddonQuantityForm
