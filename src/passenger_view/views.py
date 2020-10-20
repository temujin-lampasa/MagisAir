from django.shortcuts import render


# Create your views here.
def pass_home_view(request, *args, **kwargs):
    return render(request, 'passenger_view/home_view.html', {})
