from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from appointment.models import Appointment
from client.models import Client
from case.models import Case
from timeslot.models import TimeSlot
from speciality.models import Speciality
from lawyer.models import Lawyer

@login_required
def client_appointments(request):
    client = Client.objects.get(user=request.user)
    appointments = Appointment.objects.filter(client=client)
    return render(request, 'client/appointments.html', {'appointments': appointments})


# i am storing the values of the selected choices for lawyer and case here. i will explain it better in class. this is confusing so i have to use chat gpt to remember context. cause upon refreshing my page would reset to default values
@login_required
def book_appointment(request):
    client = Client.objects.get(user=request.user)
    specialities = Speciality.objects.all()
    cases = Case.objects.filter(client=client)

    selected_speciality_id = None
    selected_case_id = None
    selected_lawyer_id = None
    timeslots = None

    if request.method == 'GET':#this is where i am reloading the page and remembering the speciality choice
        speciality_id = request.GET.get('speciality_id')
        if speciality_id:
            selected_speciality_id = int(speciality_id)

    elif request.method == 'POST':
        action = request.POST.get('action')

        speciality_id = request.POST.get('speciality_id')
        case_id = request.POST.get('case_id')
        lawyer_id = request.POST.get('lawyer_id')
        timeslot_id = request.POST.get('timeslot_id')

        if speciality_id:
            selected_speciality_id = int(speciality_id)
        if case_id:
            selected_case_id = int(case_id)
        if lawyer_id:
            selected_lawyer_id = int(lawyer_id)

        if action == 'filter':
            if lawyer_id:
                timeslots = TimeSlot.objects.filter(
                    booked=False,
                    lawyer_id=lawyer_id
                )

        elif action == 'book':
            case = Case.objects.get(id=case_id, client=client)
            timeslot = TimeSlot.objects.get(
                id=timeslot_id,
                booked=False,
                lawyer_id=lawyer_id
            )

            Appointment.objects.create(
                client=client,
                case=case,
                timeslot=timeslot,
                status='Scheduled'
            )

            timeslot.booked = True
            timeslot.save()

            return redirect('client_appointments')

    if selected_speciality_id:#here the lawyers and the table are being filtered
        lawyers = Lawyer.objects.filter(speciality_id=selected_speciality_id)
    else:
        lawyers = Lawyer.objects.all()

    context = {
        'specialities': specialities,
        'cases': cases,
        'lawyers': lawyers,
        'timeslots': timeslots,
        'selected_speciality_id': selected_speciality_id,
        'selected_case_id': selected_case_id,
        'selected_lawyer_id': selected_lawyer_id,
    }
    return render(request, 'client/book_appointment.html', context)


@login_required
def client_cases(request):
    client = Client.objects.get(user=request.user)
    cases = Case.objects.filter(client=client)
    specialities = Speciality.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        speciality_id = request.POST.get('speciality_id')

        if title and speciality_id:
            speciality = Speciality.objects.get(id=speciality_id)
            Case.objects.create(
                title=title,
                client=client,
                speciality=speciality
            )
            return redirect('client_cases')

    context = {
        'cases': cases,
        'specialities': specialities,
    }
    return render(request, 'client/cases.html', context)