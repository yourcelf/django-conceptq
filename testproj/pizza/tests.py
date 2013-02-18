from datetime import datetime

from django.test import TestCase
from django.db.models import Q, F

from pizza.models import *
from conceptq import prefix

class TestPrefixQs(TestCase):
    def setUp(self):
        self.tomatoes = Topping.objects.create(name="tomatoes",
                savory=True, introduced=datetime(1900, 1, 1))
        self.pineapples = Topping.objects.create(name="pineapples",
                sweet=True, introduced=datetime(1960, 1, 1))
        self.peppers = Topping.objects.create(name="peppers",
                spicy=True, savory=True, introduced=datetime(1930, 1, 1))
        self.sausage = Topping.objects.create(name="sausage",
                spicy=True, savory=True, meaty=True, 
                introduced=datetime(2000, 1, 1))
        self.tofu = Topping.objects.create(name="tofu",
                introduced=datetime(2010, 1, 1))

        self.saltysweet = Pizza.objects.create()
        self.saltysweet.toppings = [self.tomatoes, self.pineapples]

        self.bland = Pizza.objects.create()
        self.bland.toppings = [self.tofu]

        self.meaty = Pizza.objects.create()
        self.meaty.toppings = [self.sausage, self.peppers, self.tomatoes]


    def test_prefix(self):
        """
        Tests that 1 + 1 always equals 2.
        """
        self.assertEquals(
            unicode(prefix("before", Q(this="that"))),
            unicode(Q(before__this="that"))
        )
        self.assertEquals(
            unicode(prefix("p", Q(Q(a="b") | Q(c="d"), Q(that="ok") | ~Q(that="ok")))),
            unicode(Q(Q(p__a="b") | Q(p__c="d"), Q(p__that="ok") | ~Q(p__that="ok")))
        )
        self.assertEquals(prefix("p", Q(a=F("b"))).children[0][1].name, "p__b")

    def test_concept_decorator(self):
        self.assertEquals(
                set(list(Topping.objects.bland())),
                set([self.tofu]))
        self.assertEquals(
                unicode(Topping.objects.bland().q),
                unicode(Q(sweet=False, savory=False, spicy=False)))
        self.assertEquals(
                set(list(Pizza.objects.bland())),
                set([self.bland]))
        self.assertEquals(
                set(list(Pizza.objects.vegetarian())),
                set([self.saltysweet, self.bland]))
        
