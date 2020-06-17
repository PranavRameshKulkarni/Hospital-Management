from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View
from hospital.models import Doctor
from .models import Appointment
from django.contrib.auth.models import User

class AppointmentView(View):
    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.all().values('user_id')
        print(doctors)
        names1 = []
        
        for i in doctors:
            names1.append(User.objects.get(id = i['user_id']))
        context = {
            'doctors': names1
        }
        return render(request, "appointment/index.html", context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        user_id = request.POST.get('doctor')
        doctor_id = Doctor.objects.get(user_id = user_id)
        date = request.POST.get('date')
        time = request.POST.get('time')
        note = request.POST.get('note')
        if doctor_id:
            doctor = get_object_or_404(Doctor, id=doctor_id.id)

        if(name and phone and email and doctor and date and time):
            Appointment.objects.create(
                name=name, phone=phone, email=email, doctor=doctor, date=date, time=time, note=note)
            messages.success(request,'Appointment done successfully')
        return redirect('appointment')
