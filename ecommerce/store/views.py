from django.shortcuts import render
from django.http import JsonResponse
import json
from .models import *


# Create your views here.
def store(request):
    products = Product.objects.all()
    context = {'products': products}
    return render(request, 'store/store.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitems_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/cart.html', context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitems_set.all()
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}
    context = {'items': items, 'order': order}
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productid = data['productId']
    action = data['action']
    print('Action: ', action)
    print('product Id: ', productid)

    customer = request.user.customer
    product = Product.objects.get(id=productid)
    order, created = Order.objects.get_or_create(customer=Customer, complete=False)
    orderitems, created = OrderItems.objects.get_or_create(Order=Order, product=Product)

    if action == 'add':
        OrderItems.quantity = (OrderItems.quantity + 1)
    elif action == 'remove':
        OrderItems.quantity = (OrderItems.quantity - 1)
    orderitems.save()

    if orderitems.quantity <= 0:
        orderitems.delete()

    return JsonResponse('Item was added', safe=False)
