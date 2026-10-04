import base64
import hashlib
import hmac
import json
import uuid
from decimal import Decimal

from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem


def _esewa_signature(message):
    digest = hmac.new(
        settings.ESEWA_SECRET_KEY.encode(), message.encode(), hashlib.sha256
    ).digest()
    return base64.b64encode(digest).decode()


def _esewa_payment_data(request, order):
    total = f'{Decimal(order.get_total_cost()):.2f}'
    transaction_uuid = order.transaction_uuid
    product_code = settings.ESEWA_PRODUCT_CODE
    signed_field_names = 'total_amount,transaction_uuid,product_code'
    message = (
        f'total_amount={total},transaction_uuid={transaction_uuid},'
        f'product_code={product_code}'
    )
    return {
        'amount': total,
        'tax_amount': '0',
        'total_amount': total,
        'transaction_uuid': transaction_uuid,
        'product_code': product_code,
        'product_service_charge': '0',
        'product_delivery_charge': '0',
        'success_url': request.build_absolute_uri(
            reverse('orders:esewa_success')
        ),
        'failure_url': request.build_absolute_uri(
            reverse('orders:esewa_failure')
        ),
        'signed_field_names': signed_field_names,
        'signature': _esewa_signature(message),
    }


def order_create(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, 'Your cart is empty.')
        return redirect('menu:menu_list')

    initial = {}
    if request.user.is_authenticated:
        initial = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            if request.user.is_authenticated:
                order.user = request.user
            order.save()
            for cart_item in cart:
                OrderItem.objects.create(
                    order=order,
                    menu_item=cart_item['item'],
                    price=cart_item['price'],
                    quantity=cart_item['quantity'],
                )
            order.transaction_uuid = str(uuid.uuid4())
            order.save(update_fields=['transaction_uuid'])
            return render(request, 'orders/esewa_payment.html', {
                'order': order,
                'payment_data': _esewa_payment_data(request, order),
                'payment_url': settings.ESEWA_PAYMENT_URL,
            })
    else:
        form = OrderCreateForm(initial=initial)

    return render(request, 'orders/order_create.html', {'cart': cart, 'form': form})


def order_created(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'orders/order_created.html', {'order': order})


def esewa_success(request):
    encoded_data = request.GET.get('data', '')
    try:
        padding = '=' * (-len(encoded_data) % 4)
        payload = json.loads(base64.b64decode(encoded_data + padding).decode())
        order = get_object_or_404(
            Order, transaction_uuid=payload['transaction_uuid']
        )
        signed_field_names = payload['signed_field_names']
        message = ','.join(
            f'{field}={payload[field]}' for field in signed_field_names.split(',')
        )
        valid_signature = hmac.compare_digest(
            payload['signature'], _esewa_signature(message)
        )
        valid_payment = (
            payload['status'] == 'COMPLETE'
            and payload['product_code'] == settings.ESEWA_PRODUCT_CODE
            and Decimal(payload['total_amount']) == Decimal(order.get_total_cost())
        )
        if not (valid_signature and valid_payment):
            raise ValueError('Invalid eSewa payment response')
    except (KeyError, TypeError, ValueError, json.JSONDecodeError,
            base64.binascii.Error, UnicodeDecodeError):
        return render(request, 'orders/payment_failed.html', status=400)

    order.payment_status = 'paid'
    order.status = 'confirmed'
    order.save(update_fields=['payment_status', 'status', 'updated_at'])
    Cart(request).clear()
    return redirect('orders:order_created', order_id=order.id)


def esewa_failure(request):
    transaction_uuid = request.GET.get('transaction_uuid')
    if transaction_uuid:
        Order.objects.filter(transaction_uuid=transaction_uuid).update(
            payment_status='failed'
        )
    return render(request, 'orders/payment_failed.html')


@login_required
def order_history(request):
    orders = request.user.orders.all()
    return render(request, 'orders/order_history.html', {'orders': orders})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'orders/order_detail.html', {'order': order})
