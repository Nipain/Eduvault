from django.db import models
from students.models import Student

class Teacher(models.Model):
    name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)

class Attendance(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    date = models.DateField()
    status = models.CharField(max_length=10)