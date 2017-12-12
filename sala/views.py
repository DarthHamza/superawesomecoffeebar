from django.shortcuts import render, redirect
from coffee.models import Coffee
from .models import Cart, CartItem

def add(request):
	if request.user.is_anonymous:
		return redirect("coffee:login")
	
	cart, created = Cart.objects.get_or_create(user=request.user)
	item = request.GET.get('item_id')
	qty = request.GET.get('qty', 1)

	if item:
		coffee = Coffee.objects.get(id=item)
		cart_item, created = CartItem.objects.get_or_create(cart=cart, item=coffee)
		if int(qty)<1:
			cart_item.delete()
		else:
			cart_item.quantity = int(qty)
			cart_item.save()
	return render(request, 'cart.html', {'cart':cart})