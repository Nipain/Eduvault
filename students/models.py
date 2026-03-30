from django.db import models
import random
import string
from datetime import datetime


class Class(models.Model):
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name


class Student(models.Model):
    RELATION_CHOICES = [
        ("father", "Father"),
        ("mother", "Mother"),
        ("other", "Other"),
    ]

    name = models.CharField(max_length=100)
    guardian_name = models.CharField(max_length=100)

    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)
    roll_number = models.CharField(max_length=50)

    admission_date = models.DateField()

    unique_id = models.CharField(max_length=50, unique=True, blank=True)

    address = models.TextField()
    guardian_phone = models.CharField(max_length=15)

    guardian_relation = models.CharField(max_length=10, choices=RELATION_CHOICES)
    guardian_relation_other = models.CharField(max_length=50, blank=True, null=True)

    opted_transport = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            year = self.admission_date.year

            random_code = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=3)
            )

            class_name = self.student_class.name

            self.unique_id = f"{year}/{random_code}/{class_name}/{self.roll_number}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.name} ({self.unique_id})"
    
    class Meta:
        unique_together = ['student_class', 'roll_number']