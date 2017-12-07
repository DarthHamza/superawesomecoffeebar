from django.db import models
from django.contrib.auth.models import User

class Bean(models.Model):
	name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=20, decimal_places=3)

	def __str__(self):
		return self.name

class Roast(models.Model):
	name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=20, decimal_places=3)

	def __str__(self):
		return self.name

class Syrup(models.Model):
	name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=20, decimal_places=3)

	def __str__(self):
		return self.name

class Powder(models.Model):
	name = models.CharField(max_length=120)
	price = models.DecimalField(max_digits=20, decimal_places=3)

	def __str__(self):
		return self.name

class Coffee(models.Model):
	creator = models.ForeignKey(User, on_delete=models.PROTECT)
	name = models.CharField(max_length=255)
	espresso_shots = models.PositiveIntegerField(default=1)
	bean = models.ForeignKey(Bean, on_delete=models.PROTECT)
	roast = models.ForeignKey(Roast, on_delete=models.PROTECT)
	powders = models.ManyToManyField(Powder, blank=True)
	syrups = models.ManyToManyField(Syrup, blank=True)
	water = models.FloatField(default=0.100)
	steamed_milk = models.BooleanField(default=False)
	foam = models.FloatField(default=0.150)
	extra_instructions = models.TextField(null=True, blank=True)
	price = models.DecimalField(max_digits=20, decimal_places=3, null=True)

	def __str__(self):
		return self.name