from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
import passenger_view.models as models


def index(request):
    return HttpResponse("Hello, world. You're at the crew assignments index.")


class HomeView(View):
    template_name = 'crew_assignments/home_view.html'
    crew_list = models.Crew.objects.all()
    flight_list = models.ScheduledFlight.objects.all()
    context = {'crew_list': crew_list, 'flight_list': flight_list}

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, self.context)
