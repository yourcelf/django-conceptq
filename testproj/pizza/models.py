from datetime import datetime
from django.db import models
from django.db.models import Q

from conceptq import concept

class ToppingManager(models.Manager):
    @concept
    def salty_sweet(self):
        return Q(sweet=True, savory=True)

    @concept
    def bland(self):
        return Q(sweet=False, savory=False, spicy=False)

    @concept
    def classic(self, cutoff=None):
        cutoff = cutoff or datetime(2000, 1, 1)
        return Q(age__lte=cutoff)

    @concept
    def meaty(self):
        return Q(meaty=True)


class Topping(models.Model):
    name = models.CharField(max_length=50)
    savory = models.BooleanField()
    sweet = models.BooleanField()
    spicy = models.BooleanField()
    meaty = models.BooleanField()
    introduced = models.DateTimeField()

    objects = ToppingManager()

    def __unicode__(self):
        return self.name

class PizzaManager(models.Manager):
    def salty_sweet(self):
        return self.filter(Topping.objects.salty_sweet().via("toppings"))

    def bland(self):
        return self.filter(Topping.objects.bland().via("toppings"))

    def classic(self):
        return self.filter(Topping.objects.classic(datetime(1990, 1, 1)).via("toppings"))

    def vegetarian(self):
        return self.filter(~Topping.objects.meaty().via("toppings"))

class Pizza(models.Model):
    toppings = models.ManyToManyField(Topping)

    objects = PizzaManager()

    def __unicode__(self):
        return u", ".join([unicode(s) for s in self.toppings])
