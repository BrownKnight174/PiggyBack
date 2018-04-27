from django.db import models
from django.contrib.auth.models import User


class Traveller(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    pnr_number = models.CharField(max_length=50)
    city_of_travel = models.CharField(max_length=25)
    date_of_travel = models.DateField('Date of Travel')
    address = models.TextField()
    aadhar_no = models.CharField(max_length=12, null=True)
    aadhar_name = models.CharField(max_length=30, null=True)

    def __str__(self):
        return "User: " + self.user.username + " | Travelling to: " + self.city_of_travel
