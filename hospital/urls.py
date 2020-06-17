from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='index'),
    path('services/', views.ServiceListView.as_view(), name="services"),
    path('services/<int:pk>/', views.ServiceDetailView.as_view(),
         name="service_details"),
    path('doctors/', views.DoctorListView.as_view(), name="doctors"),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(),
         name="doctor_details"),
    path('faqs/', views.FaqListView.as_view(), name="faqs"),
    path('gallery/', views.GalleryListView.as_view(), name="gallery"),
    path('contact/', views.ContactView.as_view(), name="contact"),
    path('doctor_login/', views.DoctorLoginView.as_view(), name = 'doctor_login'),
    path('patient_login/', views.PatientLoginView.as_view(), name = 'patient_login'),
    path('register/', views.RegisterView.as_view(), name = 'register'),
    path('logout/', views.logoutView, name = 'logout'),
    path('patient_details/', views.PatientDetailsView.as_view(), name = 'patient_details'),
    path('doctor_appoint/', views.DoctorAppoint.as_view(), name = 'doctor_appoint'),
    path('prescribe/', views.PrescribeView.as_view(), name = 'prescribe'),
path('patient_prescreptions/',views.Patientprescreptions.as_view(), name = 'patient_prescreptions'),
]
