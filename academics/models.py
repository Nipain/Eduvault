from django.db import models
from students.models import Student

class Subject(models.Model):
    name = models.CharField(max_length=100)

class Exam(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()

class Mark(models.Model):
    student = models.ForeignKey(Student,on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,on_delete=models.CASCADE)
    marks = models.IntegerField()