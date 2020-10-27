from django.urls import path
from . import views

app_name = 'crew_assignments'
urlpatterns = [
    path('', views.HomeView.as_view(), name='crew_home'),
    path('crew/<int:crew_id>', views.CrewDetail.as_view(), name='crew_detail'),
]
