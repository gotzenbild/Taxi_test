from django.urls import reverse
from django.db import models

# Create your models here.


class Car(models.Model):
    id = models.AutoField(primary_key=True)
    ordered = models.BooleanField(default=False)
    brand = models.CharField(max_length=100)


class Order(models.Model):
    id = models.AutoField(primary_key=True)
    client_name = models.CharField(max_length=100)
    client_phone = models.CharField(max_length=17)
    address = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    desired_time = models.TimeField()
    car = models.ForeignKey(Car, on_delete=models.CASCADE, null=True)

    def order_details_url(self):
        return reverse('details', kwargs={'order_id': self.id})

    def order_delete_url(self):
        return reverse('delete', kwargs={'order_id': self.id})

