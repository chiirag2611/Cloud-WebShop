from django.shortcuts import redirect
from django.shortcuts import render
import json
from django.http import JsonResponse
from django.core.mail import send_mail
from .models import Payment
from django.http import HttpResponse 
from cart.models import CartItem
from .forms import OrderForm
import datetime
from .models import Order,OrderProduct,Payment
from django.views.decorators.csrf import csrf_exempt
import logging

logger = logging.getLogger(__name__)  # Django logging

# Create your views here.
@csrf_exempt
def payments(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON from AJAX request

            # ✅ Ensure required fields exist
            if not data.get('email') or not data.get('name') or not data.get('address'):
                return JsonResponse({"success": False, "message": "Missing required user information."})

            # ✅ Save Payment Details First
            payment = Payment.objects.create(
                payment_id=data.get('paymentID'),
                order_number=data.get('orderNumber'),
                payment_method="PayPal",
                amount_paid=data.get('amount'),
                currency=data.get('currency', 'EUR'),
                status=data.get('status'),
            )
            payment.save()

            # ✅ Create the Order after payment
            order = Order.objects.create(
                order_number=data.get('orderNumber'),
                name=data.get('name'),
                email=data.get('email'),
                address=data.get('address'),
                order_total=float(data.get('amount')),
                status="New",
                is_ordered=True,
                payment=payment  # Link payment
            )
            order.save()

            # ✅ Store order_number in session before redirecting to payments.html
            request.session['order_number'] = data.get('orderNumber')

            # ✅ Fetch cart items and create OrderProduct entries
            cart_items = CartItem.objects.all()
            for item in cart_items:
                order_product = OrderProduct.objects.create(
                    order=order,
                    payment=payment,
                    product=item.product,
                    variation=item.variations.first(),
                    color="Default",
                    size="Default",
                    quantity=item.quantity,
                    product_price=item.product.price,
                    ordered=True
                )
                order_product.save()

                # ✅ Reduce stock for each product
                product = item.product
                product_stock_before = product.stock
                product.stock -= item.quantity
                if product.stock < 0:
                    product.stock = 0  # Prevent negative stock
                product.save()

                logger.info(f"Updated stock for {product.product_name}: {product_stock_before} -> {product.stock}")

            # ✅ Clear Cart
            cart_items.delete()
            send_mail(
                            subject="Order Confirmation",
                            message=f"Hello {data.get('name')},\n\nThank you for your order!\n\nYour Order Number: {data.get('orderNumber')}\nTotal: €{data.get('amount')}\n\nWe will notify you once your order is shipped.\n\nBest Regards,\nYour Store Team",
                            from_email="webshop.his@gmail.com",
                            recipient_list=[data.get('email')],
                            fail_silently=False,
                        )
            return JsonResponse({"success": True, "message": "Payment recorded, Order placed, stock updated."})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    # ✅ Retrieve order_number from session when rendering payments.html
    order_number = request.session.get('order_number', None)
    return render(request, 'orders/payments.html', {'order_number': order_number})

@csrf_exempt
def place_order(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Parse JSON from AJAX request

            # Create order entry
            order = Order.objects.create(
                order_number=data.get('orderNumber'),
                name=data.get('name'),
                email=data.get('email'),
                address=data.get('address'),
                order_total=float(data.get('total')),
                status="New",
                is_ordered=True
            )
            order.save()

            return JsonResponse({"success": True, "message": "Order placed successfully."})

        except Exception as e:
            return JsonResponse({"success": False, "message": str(e)})

    return JsonResponse({"success": False, "message": "Invalid request method."})


