from django.db import models

class Plan(models.Model):

    name = models.CharField(max_length=50)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    max_students = models.IntegerField()
    duration_days = models.IntegerField()

    def __str__(self):
        return self.name
    

class Subscription(models.Model):

    school = models.ForeignKey("tenants.School", on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)

    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()

    active = models.BooleanField(default=True)