from django.urls import path

from . import views

app_name='coffee'

urlpatterns = [
	path('create_coffee/', views.create_coffee, name='create-coffee'),
	path('get_price/', views.get_price, name='get-price'),

    path('signup/', views.usersignup, name='signup'),
    path('login/', views.userlogin, name='login'),
    path('logout/', views.userlogout, name='logout'),

    path('coffee_list/', views.coffee_list, name='coffee_list'),
    path('coffee_detail/<int:pk>/', views.coffee_detail, name='coffee_detail'),
]