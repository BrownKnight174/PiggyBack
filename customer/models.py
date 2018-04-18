from django.db import models
from django.contrib.auth.models import User


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    order_summ = models.TextField()
    order_status = models.TextField()
    delivery_date = models.DateTimeField('Delivery Date')
    receive_date = models.DateTimeField('Receive Date')


class Customer(models.Model):
    customer_no = models.AutoField(primary_key=True)
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15)
    order_summary = models.TextField()


class Connector(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    connection_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    traveller = models.ForeignKey('traveller.Traveller', on_delete=models.CASCADE)
