from django.db import models
from django.contrib.auth.models import User
from traveller.models import Traveller
import smtplib as smtp
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    product_name = models.TextField()
    product_url = models.TextField()
    status = models.CharField(max_length=20)
    fee = models.FloatField()
    creation_time = models.DateTimeField('Order Creation Time')
    delivery_date = models.DateField('Delivery Date', null=True)
    receive_date = models.DateField('Receive Date', null=True)

    def __str__(self):
        return self.product_name


class Customer(models.Model):
    customer_no = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True)
    city = models.CharField(max_length=20)

    def __str__(self):
        return "User: " + self.user.username + " | Delivery in: " + self.city

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        orderConfEmail(self.user.username)


class Connector(models.Model):
    connection_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    traveller = models.ForeignKey(Traveller, on_delete=models.CASCADE)

    def __str__(self):
        return "Customer: " + self.customer.user.username + " | Traveller: " + self.traveller.user.username

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        sendEmails(self)


def orderConfEmail(id_to):
    id_from = "parcelpanther@gmail.com"
    password = "Snu@1234"
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart()
    message['Subject'] = "Waiting for a traveller"
    message['from'] = id_from
    message['to'] = id_to
    body = "Hi\nYour order has been placed successfully.Order details are shared below.We are looking for a traveller to carry your product.\nWe will get back to you once we find a traveller\n"
    message.attach(MIMEText(body, 'plain'))
    server = smtp.SMTP(smtp_server, 587)
    server.starttls()
    server.login(id_from, password)
    server.sendmail(id_from, id_to, message.as_string())
    server.quit()


def sendEmails(connector):
    customerEmailID = connector.customer.user.username
    travellerEmailID = connector.traveller.user.username

    updateCustomer(customerEmailID)
    updateTraveller(travellerEmailID)

def updateCustomer(id_to):
    id_from = "parcelpanther@gmail.com"
    password = "Snu@1234"
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart()
    message['Subject'] = "Traveller found"
    message['from'] = id_from
    message['to'] = id_to
    body = "Hi\nWe have found a traveller who will bw carrying your product.The details of the traveller are shared below\n"
    message.attach(MIMEText(body, 'plain'))
    server = smtp.SMTP(smtp_server, 587)
    server.starttls()
    server.login(id_from, password)
    server.sendmail(id_from, id_to, message.as_string())
    server.quit()

def updateTraveller(id_to):
    id_from = "parcelpanther@gmail.com"
    password = "Snu@1234"
    smtp_server = "smtp.gmail.com"
    message = MIMEMultipart()
    message['Subject'] = "We have a product for you to bring back"
    message['from'] = id_from
    message['to'] = id_to
    body = "Hi\nWe are sending you this mail to notify you that you will be bringing back the following product(Details are shared below)\n"
    message.attach(MIMEText(body, 'plain'))
    server = smtp.SMTP(smtp_server,587)
    server.starttls()
    server.login(id_from, password)
    server.sendmail(id_from, id_to, message.as_string())
    server.quit()
