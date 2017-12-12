from django.shortcuts import render, redirect
from .forms import UserSignupForm, UserLoginForm, CoffeeForm
from django.contrib.auth import authenticate, login, logout
from decimal import Decimal
from django.http import JsonResponse
from .models import Bean,Roast,Syrup,Powder, Coffee
import json

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

def get_price(request):
	total_price = Decimal(0)

	bean_id = request.GET.get("bean")
	if bean_id:
		total_price += Bean.objects.get(id=bean_id).price

	roast_id = request.GET.get("roast")
	if roast_id:
		total_price += Roast.objects.get(id=roast_id).price

	syrups = json.loads(request.GET.get("syrups"))
	for syrup_id in syrups:
		total_price += Syrup.objects.get(id=syrup_id).price

	powders = json.loads(request.GET.get("powders"))
	for powder_id in powders:
		total_price += Powder.objects.get(id=powder_id).price

	milk = request.GET.get("milk")
	if milk == 'true':
		total_price += Decimal(0.100)

	shots = request.GET.get("shots")
	if shots:
		total_price += Decimal(int(shots)*0.250)

	return JsonResponse(round(total_price, 3), safe=False)

def coffee_list(request):
	if request.user.is_anonymous:
		return redirect("coffee:login")
	coffee_list = Coffee.objects.filter(creator=request.user)
	return render(request, 'coffee_list.html', {"coffee_list":coffee_list})

def coffee_detail(request, pk):
	if request.user.is_anonymous:
		return redirect("coffee:login")
	coffee = Coffee.objects.get(pk=pk)
	if not (request.user.is_staff or request.user==coffee.creator):
		return redirect('/you/shall/not/pass/')
	return render(request, 'coffee_detail.html', {"coffee":coffee})