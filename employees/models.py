from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Employee(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    position = models.CharField(max_length=100, blank=True)
    date_joined = models.DateField(default=timezone.now)

    def __str__(self):
        return self.user.username

class Attendance(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.now)
    status = models.CharField(max_length=10, choices=[('Present','Present'),('Absent','Absent')])

    def __str__(self):
        return f"{self.employee.user.username} - {self.date} - {self.status}"
