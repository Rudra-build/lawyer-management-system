from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_page, name='empty'),
    path('login/', views.login_page, name='login_page'),
    path('logout/', views.logout_user, name='logout_user'),
    path('signup/', views. register_client, name='register_client'),
    path('home/', views.dashboard_home, name='dashboard_home'),

    path('report/completed/', views.report_completed_appointments, name='report_completed_appointments'),
    path('report/revenue/', views.report_lawyer_revenue, name='report_lawyer_revenue'),
    path('report/distribution/', views.report_appointment_distribution, name='report_appointment_distribution')
]