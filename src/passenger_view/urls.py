from django.urls import path
from .views import (
    pass_home_view
)


app_name = 'passenger_view'
urlpatterns = [
    path('', pass_home_view, name='pass_home'),
]
