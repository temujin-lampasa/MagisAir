from django.urls import path
from .views import (
    home_view,
    pass_info_view,
    FlightSelectView
                    )


app_name = 'passenger_view'
urlpatterns = [
    path('', home_view, name='pass_home'),
    path('flights/', FlightSelectView.as_view(), name='pass_flights'),
    # path('flights/<id:pk>'),
    path('pass_info/', pass_info_view, name='pass_info')
]
