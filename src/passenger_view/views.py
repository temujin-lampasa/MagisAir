from django.shortcuts import render
from .models import Airport
from .forms import FlightSearchForm


# Create your views here.
def pass_home_view(request, *args, **kwargs):
    form = FlightSearchForm(request.POST or None)
    if form.is_valid():
        print(form.cleaned_data)
    context = {'form': form}
    return render(request, 'passenger_view/home_view.html', context)
