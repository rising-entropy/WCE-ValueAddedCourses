from django.db import models
from django.contrib.auth.models import User
User._meta.get_field('email')._unique = True
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator

# Create your models here.
from django.db.models import OneToOneField

class student(models.Model):
    user: OneToOneField = models.OneToOneField(User, on_delete=models.CASCADE)
    designation = models.CharField(max_length=20)
    organisation = models.CharField(max_length=100)
    address = models.CharField(max_length=400)
    phoneNumber = models.CharField(max_length=15, default="1234567890")
    PaidAttendencePython=models.BooleanField(default=False)
    PaidAttendenceCertificatePython=models.BooleanField(default=False)
    PaidAttendenceDL=models.BooleanField(default=False)
    PaidAttendenceCertificateDL=models.BooleanField(default=False)
    profilePicture = models.CharField(max_length=500)
    
    def __str__(self):
        return self.user.username

class enrolledStudent(models.Model):
    amount     = models.CharField(max_length=100)
    paymentID  = models.CharField(max_length=100)
    screenShot = models.CharField(max_length=500)
    paymentType = models.CharField(max_length=100, default="Net Banking")
    enrolled_stud = models.ForeignKey(student, on_delete=models.CASCADE)

    def __str__(self):
        return self.enrolled_stud.user.username