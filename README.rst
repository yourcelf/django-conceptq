django-conceptq
===============

``conceptq`` is a small, simple utility for pullng portable, composable
"concepts" out of Django ORM queries, using Q objects.  

the problem
-----------

The problem: say you have a bit of logic that applies to a model -- for example, a pizza topping is "savory" if it's salty or spicy, but not sweet.  The models::

    class ToppingManager(models.Manager)
        def savory(self):
            return self.filter(Q(savory=True) | Q(salty=True), sweet=False)

    class Topping(models.Model):
        savory = models.BooleanField()
        salty = models.BooleanField()
        sweet = models.BooleanField()

        objects = ToppingManager()

    class Pizza(models.Model):
        toppings = models.ManyToManyField(Topping)

This works great, until you want to carry that concept over to "Pizza" classes.
How do you say that a pizza is savory?  It's savory if its toppings are.  But
when our logic for the toppings is bound up in the Topping manager, we end up
having to duplicate it in the Pizza manager too::

    class PizzaManager(models.Manager):
        def savory(self):
            return self.filter(Q(topping__savory=True) | Q(topping__salty=True),
                topping__sweet=False)

With each step down the related manager chain, we're duplicating the query
logic yet again.  Not very DRY, bug magnet, etc.

conceptq
--------

``conceptq`` is primarily a single decorator, ``@concept``, that you can apply to 
a manager method.  It expects the method to return a  
`Q object <https://docs.djangoproject.com/en/1.4/topics/db/queries/#complex-lookups-with-q-objects>`_,
rather than a queryset; but it wraps the Q object in a ``filter`` call so the 
manager methods still chain like normal.  In addition, it provides a ``via`` method 
to prefix all the calls for you::

    class ToppingManager(models.Manager):
        @concept
        def savory(self):
            return Q(Q(savory=True) | Q(salty=True), sweet=False)

This can then be used this way::

    Topping.objects.savory()                # --> returns queryset
    Topping.objects.savory().q              # --> returns the Q object 
    Topping.objects.savory().via("prefix")  # --> returns Q object with
                                            #     prefixed fields

Now we can have fun across relations::

    Pizza.objects.filter(Topping.objects.savory().via("toppings"))
    Customer.objects.filter(
        Topping.objects.savory().via("favorite_pizza__toppings")
    )

And we can use the manager class as a place to build a library of higher level
concepts that can be composed together easily::

    class ToppingManager(models.Manager):
        @concept
        def savory(self):
            return Q(Q(savory=True) | Q(salty=True), sweet=False)

        @concept
        def cajun(self):
            return Q(savory=True, burnt=True)

        @concept
        def high_calorie(self):
            return Q(calories__gte=300)

        @concept
        def diet_cajun(self):
            return ((self.savory().q | self.cajun().q) & ~self.high_calorie().q)


    >>> diet_cajun_pizzas = Pizza.objects.filter(
            Topping.objects.diet_cajun().via("toppings"))

For more, see the included ``testproject`` and the only 40 lines of source code.

license
-------

Copyright (c) 2013, Charlie DeTar
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met: 

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer. 
2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution. 

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND
ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR
ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES
(INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND
ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
(INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS
SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

The views and conclusions contained in the software and documentation are those
of the authors and should not be interpreted as representing official policies, 
either expressed or implied, of the FreeBSD Project.

