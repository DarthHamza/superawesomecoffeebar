from django.shortcuts import render, redirect
from .forms import UserSignupForm, UserLoginForm, CoffeeForm
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal

def usersignup(request):
	context = {}
	form = UserSignupForm()
	context['form'] = form
	if request.method == 'POST':
		form = UserSignupForm(request.POST)
		if form.is_valid():
			user = form.save()
			username = user.username
			password = user.password

			user.set_password(password)
			user.save()

			auth = authenticate(username=username, password=password)
			login(request, auth)
			return redirect('/')
		return redirect('coffee:signup')
	return render(request, 'signup.html', context)

def userlogin(request):
	context = {}
	form = UserLoginForm()
	context['form'] = form
	if request.method == 'POST':
		form = UserLoginForm(request.POST)
		if form.is_valid():
			username = form.cleaned_data['username']
			password = form.cleaned_data['password']

			auth = authenticate(username=username, password=password)
			if auth is not None:
				login(request, auth)
				return redirect('/')
			return redirect('coffee:login')
		return redirect('coffee:login')
	return render(request, 'login.html', context)

def userlogout(request):
	logout(request)
	return redirect('coffee:login')

def coffee_price(coffee):
	total_price = coffee.bean.price + coffee.roast.price + (coffee.espresso_shots*Decimal(0.250))
	if coffee.steamed_milk:
		total_price += Decimal(0.100)
	for powder in coffee.powders.all():
		total_price += powder.price
	for syrup in coffee.syrups.all():
		total_price += syrup.price
	return total_price


def create_coffee(request):
	context = {}
	if not request.user.is_authenticated:
		return redirect("coffee:login")
	form = CoffeeForm()
	if request.method == 'POST':
		form = CoffeeForm(request.POST)
		if form.is_valid():
			coffee = form.save(commit=False)
			coffee.creator = request.user
			coffee.save()
			form.save_m2m()
			coffee.price = coffee_price(coffee)
			coffee.save()
			return redirect('/')
	context['form']=form
	return render(request, 'create_coffee.html', context)