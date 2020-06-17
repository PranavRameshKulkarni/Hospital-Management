from django.shortcuts import render, redirect , get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from .models import Slider, Service, Doctor, Faq, Gallery, Patient, Prescribe
from django.views.generic import ListView, DetailView, TemplateView, View
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django import template
from django.contrib.auth.models import User


register = template.Library() 

@register.filter(name='has_group') 
def has_group(user, group_name):
    return user.groups.filter(name=group_name).exists() 

class HomeView(ListView):
    template_name = 'hospital/index.html'
    queryset = Service.objects.all()
    context_object_name = 'services'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context['sliders'] = Slider.objects.all()
        context['experts'] = Doctor.objects.all()
        return context


class ServiceListView(ListView):
    queryset = Service.objects.all()
    template_name = "hospital/services.html"



class ServiceDetailView(DetailView):
    queryset = Service.objects.all()
    template_name = "hospital/service_details.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["services"] = Service.objects.all()
        return context


class DoctorListView(ListView):
    template_name = 'hospital/team.html'
    queryset = Doctor.objects.all()
    paginate_by = 8


class DoctorDetailView(DetailView):
    template_name = 'hospital/team-details.html'
    queryset = Doctor.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["doctors"] = Doctor.objects.all()
        return context


class FaqListView(ListView):
    template_name = 'hospital/faqs.html'
    queryset = Faq.objects.all()


class GalleryListView(ListView):
    template_name = 'hospital/gallery.html'
    queryset = Gallery.objects.all()
    paginate_by = 9


class ContactView(TemplateView):
    template_name = "hospital/contact.html"

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        if subject == '':
            subject = "Heartcare Contact"

        if name and message and email and phone:
            send_mail(
                subject+"-"+phone,
                message,
                email,
                ['expelmahmud@gmail.com'],
                fail_silently=False,
            )
            messages.success(request, " Email hasbeen sent successfully...")

        return redirect('contact')

class DoctorLoginView(TemplateView):
    template_name = "Login/doctor_login.html"

    def post(self, request, *args, **kwargs):
        doctors = Group.objects.get(name='Doctors')
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        emails = User.objects.filter(is_active=True).values_list('email', flat=True)
        print(emails)
        username = User.objects.filter(email=email).values_list('username', flat=True)
        username = User.objects.get(email= email).username
        print('username',username)
        user = authenticate(username=username, password=password)
        # if user.groups.filter(name = groupname).exists():
        print("USER GROUPS",user.groups.all())
        if user and user.groups.filter(name = doctors).exists():    
            login(request, user)
            messages.success(request, 'Logged In!')
        else:
            messages.success(request, 'Doctor does not exist!!')
            return redirect('doctor_login')
        return redirect('index')

class PatientLoginView(TemplateView):
    template_name = "Login/patient_login.html"

    def post(self, request, *args, **kwargs):
        patients = Group.objects.get(name='Patients')
        email = request.POST.get('email')
        print(email)
        password = request.POST.get('password')
        print(password)
        username = User.objects.get(email=email).username
        user = authenticate(username=username, password=password)
        # if user.groups.filter(name = groupname).exists():
        print("USER GROUPS",user.groups.all())
        if user and user.groups.filter(name = patients).exists():
            
            login(request, user)
            messages.success(request, 'Logged In!')


        else:
            messages.success(request, 'Patient does not exist!!')
            return redirect('patient_login')
        
        return redirect('index')
        


class RegisterView(TemplateView):
    template_name = "Login/register.html"
    queryset = Doctor.objects.all()

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        password = request.POST.get('password')
        doctor_id = request.POST.get('doctor')
        note = request.POST.get('note')
        if doctor_id:
            doctor = get_object_or_404(Doctor, id=doctor_id)

        if(name and phone and email and doctor):
            user = User.objects.create_user(username=name,
                                 email=email,
                                 password=password)
            patients = Group.objects.get(name='Patients') 
            user.groups.add(patients)                   
            Patient.objects.create(
                user= user, phone=phone, doctor=doctor, notes=note)
            messages.success(request,'patient added successfully')
        return redirect('patient_login')


# class logout(View):
#     def get(self, request):
#         logout()
#         print(request.user.get_username())
#         return redirect('index')
def logoutView(request):
    logout(request)
    return redirect('index')    



class PatientDetailsView(TemplateView):
    # template_name = "patients.html"
    # getnames = Patient.objects.filter()
    # queryset = Doctor.objects.all()

    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.get(user_id = request.user.id)
        names = doctors.patient_doctor.all().values('user_id')
        names1 = []
        print('names' , names)
        for i in names:
            names1.append(User.objects.get(id = i['user_id']))

        print(names1)
        context = {
           
            'names':names1
           
        }
        print('context', context)
        return render(request, "hospital/patient.html", context)

class DoctorAppoint(TemplateView):
  
    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.get(user_id = request.user.id)
        appoint = doctors.appointments.all()
        context = {
            'appoint':appoint
        }
        return render(request,"hospital/doctor_appoint.html", context)


class PrescribeView(TemplateView):
    def get(self, request, *args, **kwargs):
        doctors = Doctor.objects.get(user_id = request.user.id)
        names = doctors.patient_doctor.all().values('user_id')
        names1 = []
        print('names' , names)
        for i in names:
            names1.append(User.objects.get(id = i['user_id']))
        context = {
           
            'names':names1
           
        }
        
        return render(request,"hospital/prescribe.html", context)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        medicine = request.POST.get('medicine')
        doctor = Doctor.objects.get(user_id = request.user.id)
        patient_user_id = request.POST.get('email')
        date = request.POST.get('date')
        note = request.POST.get('reason')
        if patient_user_id:
            patient = get_object_or_404(Patient, user_id=patient_user_id)

        if(name and date and patient and medicine):
            Prescribe.objects.create(
                doctor=doctor,patient = patient, medicine=medicine,reason=note, date=date)
            messages.success(request,'prescription added successfully')
        return redirect('index')

        
class Patientprescreptions(TemplateView):
  
    def get(self, request, *args, **kwargs):
        patients = Patient.objects.get(user_id = request.user.id)
        prescribe = Prescribe.objects.get(patient_id = patients)
        doctor = Doctor.objects.get(id = prescribe.doctor_id)
        user = User.objects.get(id = doctor.user_id)
        context = {
            'prescribes':prescribe,
            'user':user
        }
        print(prescribe.doctor)
        return render(request,"hospital/patient_prescreptions.html", context)