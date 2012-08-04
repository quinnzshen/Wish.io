from django.db import models

class User(models.Model):
    name = models.CharField(max_length=21, unique=True)
    password = models.CharField(max_length=200)
    friends = models.ManyToManyField('User', null=True, blank=True)

class Item(models.Model):
    url = models.URLField()
    price = models.DecimalField(decimal_places=2)