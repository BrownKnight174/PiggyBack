from django.db import models
from django.contrib.auth.models import User
from traveller.models import Traveller


class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    product_name = models.TextField()
    product_url = models.TextField()
    status = models.TextField()
    fee = models.FloatField()
    creation_time = models.DateTimeField('Order Creation Time')
    delivery_date = models.DateField('Delivery Date', null=True)
    receive_date = models.DateField('Receive Date', null=True)


class Customer(models.Model):
    customer_no = models.AutoField(primary_key=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=15, null=True)


class Connector(models.Model):
    order_id = models.ForeignKey(Order, on_delete=models.CASCADE)
    connection_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    traveller = models.ForeignKey(Traveller, on_delete=models.CASCADE)
