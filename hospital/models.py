from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
class Slider(models.Model):
    caption = models.CharField(max_length=150)
    slogan = models.CharField(max_length=120)
    image = models.ImageField(upload_to='sliders/')

    def __str__(self):
        return self.caption[:20]

    class Meta:
        verbose_name_plural = 'Slider'


class Service(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    items = models.ManyToManyField(to='Item',)
    thumbnail = models.ImageField(upload_to='services/')
    cover = models.ImageField(upload_to='services/')
    image1 = models.ImageField(upload_to='services/', blank=True, null=True)
    image2 = models.ImageField(upload_to='services/', blank=True, null=True)

    def __str__(self):
        return self.title


class Item(models.Model):
    title = title = models.CharField(max_length=120)

    def __str__(self):
        return self.title


class Doctor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile')
    speciality = models.CharField(max_length=120)
    picture = models.ImageField(upload_to="doctors/") 
    details = models.TextField()
    experience = models.TextField()
    expertize = models.ManyToManyField(to='Expertize', related_name='doctors')
    twitter = models.CharField(max_length=120, blank=True, null=True)
    facebook = models.CharField(max_length=120, blank=True, null=True)
    instagram = models.CharField(max_length=120, blank=True, null=True)

    def __str__(self):
        return self.user.email


class Expertize(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name


class Faq(models.Model):
    question = models.CharField(max_length=120)
    answer = models.TextField()

    def __str__(self):
        return self.question


class Gallery(models.Model):
    title = models.CharField(max_length=120)
    image = models.ImageField(upload_to="gallery/")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Galleries"


class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    phone = models.CharField(max_length=20)
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='patient_doctor')
    notes = models.CharField(max_length=120)
    def __str__(self):
        return self.user.username

class Prescribe(models.Model):
    doctor = models.ForeignKey(
        Doctor, on_delete=models.CASCADE, related_name='prescribe_doctor')
    patient =  models.ForeignKey(
        Patient, on_delete=models.CASCADE, related_name='prescribe_patient')
    medicine = models.CharField(max_length=20)
    reason =  models.CharField(max_length=20)
    date = models.DateField(default=timezone.now)
    