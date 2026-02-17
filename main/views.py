from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from client.models import Client
from lawyer.models import Lawyer 
from appointment.models import Appointment
from speciality.models import Speciality

# Create your views here.


#def home(request):
#   return render (request, 'test_home.html')

def login_page(request):
    if request.user.is_authenticated:
        return redirect('dashboard_home')
    #if already logged in, send him to home page, don't show the form
    
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request , user)
            return redirect ('dashboard_home')
        
    else:
        form = AuthenticationForm()

    return render(request , 'login_page.html' , {'form': form})

def logout_user(request):
    logout(request)
    return redirect('login_page')

def register_client(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            Client.objects.create(user = user)
            return redirect ('login_page')
        
    else:
        form = UserCreationForm ()

    return render (request , 'signup_page.html' , {'form': form})

@login_required
def dashboard_home(request):

    #lawyer home
    try:
        Lawyer.objects.get(user = request.user)
        return render (request , 'lawyer_home.html' )
    
    except Lawyer.DoesNotExist:
        pass

    #client home
    try:
        Client.objects.get(user = request.user)
        return render(request, 'client_home.html')
    
    except Client.DoesNotExist:
        pass

    #I kept having errors when super users are logged into admin and then when i redirect the page. so, this is a fallback which logs the super user out
    logout(request)
    return redirect('login_page')




# reports now
@login_required
def report_completed_appointments(request):
    appointments = None
    count = 0
    start_date = None
    end_date = None

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            appointments = Appointment.objects.filter(
                status='Completed',
                timeslot__date__gte=start_date,#gte = greater than equal to
                timeslot__date__lte=end_date #lets = less than equal to
            )
            count = appointments.count()

    context = {
        'appointments': appointments,
        'count': count,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'report_completed.html', context)


@login_required
def report_lawyer_revenue(request):
    results = []
    start_date = None
    end_date = None

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            appointments = Appointment.objects.filter(
                status='Completed',
                timeslot__date__gte=start_date,
                timeslot__date__lte=end_date
            )

            
            data = {}
            for appt in appointments:
                lawyer = appt.timeslot.lawyer
                if lawyer.id not in data:
                    data[lawyer.id] = {
                        'lawyer': lawyer,
                        'count': 0,
                        'hours': 0,
                        'revenue': 0,
                    }
                data[lawyer.id]['count'] += 1
                data[lawyer.id]['hours'] += 1      # each appointment = 1 hour
                data[lawyer.id]['revenue'] += float(lawyer.hourly_rate)

            results = list(data.values())

    context = {
        'results': results,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'report_revenue.html', context)


@login_required
def report_appointment_distribution(request):
    results = []
    start_date = None
    end_date = None

    if request.method == 'POST':
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')

        if start_date and end_date:
            appointments = Appointment.objects.filter(
                timeslot__date__gte=start_date,
                timeslot__date__lte=end_date
            )

            
            data = {}
            for appt in appointments:
                speciality = appt.case.speciality
                lawyer = appt.timeslot.lawyer

                if speciality.id not in data:
                    data[speciality.id] = {
                        'speciality': speciality,
                        'lawyers': {}
                    }

                if lawyer.id not in data[speciality.id]['lawyers']:
                    data[speciality.id]['lawyers'][lawyer.id] = {
                        'lawyer': lawyer,
                        'count': 0
                    }

                data[speciality.id]['lawyers'][lawyer.id]['count'] += 1

            
            for speciality_info in data.values():
                speciality = speciality_info['speciality']
                for lawyer_info in speciality_info['lawyers'].values():
                    results.append({
                        'speciality': speciality,
                        'lawyer': lawyer_info['lawyer'],
                        'count': lawyer_info['count'],
                    })

    context = {
        'results': results,
        'start_date': start_date,
        'end_date': end_date,
    }
    return render(request, 'report_distribution.html', context)
