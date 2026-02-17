from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from datetime import date, time, timedelta #move forward in days(i used it to genearate it later)
from .models import TimeSlot
from lawyer.models import Lawyer

# Create your views here.
@login_required
def generate_time_slots(request, lawyer_id):
    # helper to auto-generate slots for a lawyer
    #/timeslot/generate/1
    lawyer = Lawyer.objects.get(id=lawyer_id)

    start_date = date.today()
    days_ahead = 7  # next 7 days
    start_hour = 9
    end_hour = 17   # 9–17 = 9:00,10:00,...,16:00

    for day_offset in range(days_ahead):
        current_date = start_date + timedelta(days=day_offset)

        for hour in range(start_hour, end_hour):
            start_time = time(hour=hour, minute=0)

            # this is to avoid duplicates if I run this twice
            exists = TimeSlot.objects.filter(
                lawyer=lawyer,
                date=current_date,
                start_time=start_time
            ).exists()

            if not exists:
                TimeSlot.objects.create(
                    lawyer=lawyer,
                    date=current_date,
                    start_time=start_time,
                    booked=False
                )

    return redirect('lawyer_appointments')