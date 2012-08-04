from django.db import models

privacies = (
    ('public', 'public'), 
    ('private', 'private')
)


class User(models.Model):
    name = models.CharField(max_length=21, unique=True)
    password = models.CharField(max_length=200)
    friends = models.ManyToManyField('User', null=True, blank=True)

    def __unicode__(self):
        return self.name


class Item(models.Model):
    name = models.CharField(max_length=200)
    url = models.URLField()
    price = models.DecimalField(max_digits=9, decimal_places=2)
    rank = models.IntegerField(unique=True)
    wishlist = models.ForeignKey('WishList')

    def __unicode__(self):
        return self.name


class WishList(models.Model):
    name = models.CharField(max_length=200)
    privacy = models.CharField(max_length=10, choices=privacies)
    owner = models.ForeignKey('User', related_name="owner")
    members = models.ForeignKey('User', related_name="members")
    items = models.ForeignKey('Item', related_name="items", null=True, blank=True)

    def __unicode__(self):
        return self.name