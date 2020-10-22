from django.urls import path
from .views import (
    home_view,
    PassInfoView,
    FlightSelectView,
    AddonSelectView,
                    )


app_name = 'passenger_view'
urlpatterns = [
    path('', home_view, name='pass_home'),
    path('flights/', FlightSelectView.as_view(), name='pass_flights'),
    path('pass_info/', PassInfoView.as_view(), name='pass_info'),
    path('addons', AddonSelectView.as_view(), name='addon_select'),
]
