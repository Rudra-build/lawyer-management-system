from django.urls import path
from . import views

urlpatterns = [
    path('appointment/' , views.client_appointments, name='client_appointments'),
    path('book/', views.book_appointment , name='book_appointment'),
    path('cases/', views.client_cases, name='client_cases')
]