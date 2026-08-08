from django.shortcuts import render, redirect, get_object_or_404
from .models import CoffeeItem, Order, OrderItem

def coffee_list(request):
    query = request.GET.get('q', '')
    if query:
        coffees = CoffeeItem.objects.filter(name__icontains=query) | CoffeeItem.objects.filter(branch_name__icontains=query)
    else:
        coffees = CoffeeItem.objects.all()
    return render(request, 'coffee/coffee_list.html', {'coffees': coffees, 'query': query})

def add_to_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')
    coffee = get_object_or_404(CoffeeItem, id=item_id)
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    order_item, created = OrderItem.objects.get_or_create(order=order, coffee=coffee)
    if not created:
        order_item.quantity += 1
        order_item.save()
    return redirect('view_cart')

def view_cart(request):
    if not request.user.is_authenticated:
        return redirect('login')
    order, created = Order.objects.get_or_create(user=request.user, is_completed=False)
    return render(request, 'coffee/cart.html', {'order': order})

def checkout(request):
    if not request.user.is_authenticated:
        return redirect('login')
    order = get_object_or_404(Order, user=request.user, is_completed=False)
    order.is_completed = True
    order.save()
    return redirect('coffee_list')