from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from appointment.models import Appointment
from lawyer.models import Lawyer
from case.models import Case

# Create your views here.
@login_required
def lawyer_appointments(request):
    # get the lawyer linked to this user
    lawyer = Lawyer.objects.get(user=request.user)

    # get appointments where the timeslot belongs to this lawyer
    appointments = Appointment.objects.filter(timeslot__lawyer=lawyer)

    return render(request, 'lawyer/appointments.html', {
        'appointments': appointments
    })


@login_required
def lawyer_appointment_detail(request, appointment_id):
    # get the lawyer linked to this user
    lawyer = Lawyer.objects.get(user=request.user)

    # make sure the appointment belongs to this lawyer
    appointment = get_object_or_404(Appointment, id=appointment_id, timeslot__lawyer=lawyer)

    if request.method == 'POST':
        status = request.POST.get('status')
        notes = request.POST.get('notes')

        appointment.status = status
        appointment.notes = notes
        appointment.save()

        return redirect('lawyer_appointments')

    return render(request, 'lawyer/appointment_detail.html', {
        'appointment': appointment
    })


@login_required
def lawyer_cases(request):
    # get the lawyer
    lawyer = Lawyer.objects.get(user=request.user)

    # find all cases linked via appointments
    case_ids = Appointment.objects.filter(timeslot__lawyer=lawyer).values_list('case_id', flat=True)
    cases = Case.objects.filter(id__in=case_ids).distinct()

    return render(request, 'lawyer/cases.html', {'cases': cases})