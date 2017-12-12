from django.db import models
from coffee.models import Coffee
from django.contrib.auth.models import User
from django.db.models.signals import pre_save, post_save, post_delete
from decimal import Decimal

class CartItem(models.Model):
    cart = models.ForeignKey("Cart", on_delete=models.PROTECT)
    item = models.ForeignKey(Coffee, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    line_item_total = models.DecimalField(decimal_places = 3, max_digits = 20)

    def __str__(self):
        return self.item.name

def cart_item_pre_save(instance, *args, **kwargs):
	qty = instance.quantity
	if qty >= 1:
		price = instance.item.price
		total = price * qty
		instance.line_item_total = total

pre_save.connect(cart_item_pre_save,sender=CartItem)

def cart_item_reciever(instance, *args, **kwargs):
	instance.cart.calc_subtotal()

post_save.connect(cart_item_reciever,sender=CartItem)
post_delete.connect(cart_item_reciever,sender=CartItem)

class Cart(models.Model):
    user = models.ForeignKey(User, null=True, blank=True, on_delete=models.PROTECT)
    items = models.ManyToManyField(Coffee, through=CartItem)
    subtotal = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)
    delivery_total = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)
    total = models.DecimalField(decimal_places = 3, max_digits = 50, default=2.000)

    def __str__(self):
        return str(self.id)

    def calc_subtotal(self):
    	sub = Decimal(0)
    	items = self.cartitem_set.all()
    	for item in items:
    		sub += item.line_item_total
    	self.subtotal = sub
    	self.save()

def calc_delivery_total_and_total(instance, *args, **kwargs):
	instance.total = instance.subtotal + instance.delivery_total

pre_save.connect(calc_delivery_total_and_total, sender=Cart)