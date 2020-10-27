from django.urls import path
from . import views

app_name = 'crew_assignments'
urlpatterns = [
    path('', views.HomeView.as_view(), name='crew_home'),
]
