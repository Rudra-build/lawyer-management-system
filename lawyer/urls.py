from django.urls import path
from . import views

urlpatterns = [
    path('appointments/', views.lawyer_appointments, name='lawyer_appointments'),
    path('appointments/<int:appointment_id>/', views.lawyer_appointment_detail, name='lawyer_appointment_detail'),
    path('cases/', views.lawyer_cases, name='lawyer_cases'),
]