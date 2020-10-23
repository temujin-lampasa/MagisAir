from django.urls import path
from .views import (
    HomeView,
    PassInfoView,
    FlightSelectView,
    AddonSelectView,
    ConfirmView,
                    )


app_name = 'passenger_view'
urlpatterns = [
    path('', HomeView.as_view(), name='pass_home'),
    path('flights/', FlightSelectView.as_view(), name='pass_flights'),
    path('pass_info/', PassInfoView.as_view(), name='pass_info'),
    path('addons/', AddonSelectView.as_view(), name='addon_select'),
    path('confirm_booking/', ConfirmView.as_view(), name='confirmation_view')
]
