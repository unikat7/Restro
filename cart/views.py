from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from menu.models import MenuItem
from .cart import Cart


@require_POST
@login_required
def cart_add(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, id=item_id, is_available=True)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(item=item, quantity=quantity)
    messages.success(request, f'{item.name} added to your cart.')
    return redirect(request.POST.get('next') or 'cart:cart_detail')


def cart_remove(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, id=item_id)
    cart.remove(item)
    messages.info(request, f'{item.name} removed from cart.')
    return redirect('cart:cart_detail')


@require_POST
def cart_update(request, item_id):
    cart = Cart(request)
    item = get_object_or_404(MenuItem, id=item_id)
    quantity = int(request.POST.get('quantity', 1))
    cart.add(item=item, quantity=quantity, override_quantity=True)
    return redirect('cart:cart_detail')


def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/cart_detail.html', {'cart': cart})
