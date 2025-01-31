from django.shortcuts import redirect
from django.shortcuts import render
import json
from django.http import JsonResponse
from .models import Payment
from django.http import HttpResponse 
from cart.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)  # Django logging

# Create your views here.
def payments(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON from AJAX request
            payment = Payment.objects.create(
                payment_id=data.get('paymentID'),
                order_number=data.get('orderNumber'),  # ✅ Store the order number
                payment_method="PayPal",
                amount_paid=data.get('amount'),
                currency=data.get('currency', 'EUR'),
                status=data.get('status'),
            )
            payment.save()

            return JsonResponse({"success": True, "message": "Payment recorded successfully."})
        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return render(request, 'orders/payments.html')  # Show confirmation page

@csrf_exempt
def place_order(request, total=0, quantity=0):
    cart_items = CartItem.objects.all()
    cart_count = cart_items.count()
    
    if cart_count <= 0:
        return redirect('store')

    for cart_item in cart_items:
        total += cart_item.sub_total()
        quantity += cart_item.quantity

        # Log to Django logs
        logger.info(f"Product: {cart_item.product.product_name}, Price: {cart_item.product.price}, Quantity: {cart_item.quantity}")

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            data = Order()
            data.name = form.cleaned_data['name']
            data.email = form.cleaned_data['email']
            data.address = form.cleaned_data['address']
            data.order_total = total
            data.save()

            # Generate Order Number
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime.date(yr, mt, dt)
            current_date = d.strftime("%Y%m%d")  # Example: 20210305
            order_number = f"{current_date}{data.id}"
            data.order_number = order_number
            data.save()

            # ✅ Pass `order_number` to the checkout template
            return render(request, 'checkout.html', {'order_number': order_number, 'cart_items': cart_items, 'total': total})

    return redirect('checkout')

