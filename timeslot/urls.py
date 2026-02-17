from django.urls import path
from . import views

urlpatterns = [
    path('generate/<int:lawyer_id>/', views.generate_time_slots, name='generate_time_slots'),
]