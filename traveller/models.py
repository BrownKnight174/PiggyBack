from django.db import models
from django.contrib.auth.models import User
import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


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
        return str(self.pk) + " User: " + self.user.username + " | Travelling to: " + self.city_of_travel

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        registrationConf(self.user.username, self.user.first_name)


def registrationConf(id_to, first_name):
    id_from = "parcelpanther@gmail.com"
    password = "Snu@1234"
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart()
    message['Subject'] = "Successfully Registered to PiggyBack"
    message['from'] = id_from
    message['to'] = id_to
    body = "Hi " + first_name + "!\n\nYou have been successfully registered.\n\nWe'll get back to you once we find a product for you to deliver!\n\nHave a nice day!"
    message.attach(MIMEText(body, 'plain'))
    server = smtp.SMTP(smtp_server,587)
    server.starttls()
    server.login(id_from,password)
    server.sendmail(id_from,id_to,message.as_string())
    server.quit()