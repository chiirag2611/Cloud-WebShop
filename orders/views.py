from django.shortcuts import render
from django.http import HttpResponse 
from cart.models import CartItem
from .forms import OrderForm
import datetime

# Create your views here.
def place_order (request):
    current_user = request.user
    # If the cart count is less than or equal to 0, then redirect back to shop
    cart_items = CartItem.objects
    cart_count = cart_items.count()
    if cart_count <= 0:
        return redirect('store')
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form. is_valid():
            data = Order()
            data.first_name = form.cleaned_data['name']
            data.email = form. cleaned_data['email']
            data.address_line = form.cleaned_data['address']
            data.save()
            yr = int(datetime.date.today().strftime('%Y'))
            dt = int(datetime.date.today().strftime('%d'))
            mt = int(datetime.date.today().strftime('%m'))
            d = datetime. date(yr, mt, dt)
            current_date = d.strftime ("%Y%m%d") #20210305
            order_number = current_date + str(data.id)
            data.order_number = order_number 
            data.save()
            return redirect('checkout')
        else:
            return redirect('checkout')
    
