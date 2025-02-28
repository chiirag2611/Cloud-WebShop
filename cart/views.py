from django.shortcuts import render, redirect, get_object_or_404  # type: ignore
from store.models import Product, Variation
from .models import Cart, CartItem
from django.http import HttpResponse # type: ignore

def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    product_variation_list = []
    for item in  request.POST:
        key = item
        value = request.POST[key]
        if value and key != 'csrfmiddlewaretoken':  # Exclude CSRF token
            try:
                variation = Variation.objects.get(
                    product=product, 
                    variation_category__iexact=key, 
                    variation_value__iexact=value
                ) 
                product_variation_list.append(variation)
            except:
                pass 

    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(cart_id=_cart_id(request))
    cart.save()

    is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product=product, cart=cart)
        existing_variation_list = []
        existing_item_ids = []
        for item in cart_item:
            existing_variation = list(item.variations.all())
            existing_variation_list.append(list(existing_variation))
            existing_item_ids.append(item.id)

        print(existing_variation_list)

        if product_variation_list in existing_variation_list:
            index = existing_variation_list.index(product_variation_list)
            item_id = existing_item_ids[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity=1, cart=cart)
            if product_variation_list:
                item.variations.add(*product_variation_list)
    else:
        cart_item = CartItem.objects.create(product = product, quantity = 1, cart = cart)
        if len(product_variation_list) > 0:
            cart_item.variations.clear()
            cart_item.variations.add(*product_variation_list)
        cart_item.save()
    
    return redirect('cart')

def update_cart(request, product_id, action):
    product = Product.objects.get(id=product_id)
    cart = Cart.objects.get(cart_id=_cart_id(request))

    cart_item = CartItem.objects.get(product=product, cart=cart)

    if action == 'increase':
        cart_item.quantity += 1
    elif action == 'decrease' and cart_item.quantity > 1:
        cart_item.quantity -= 1
    cart_item.save()

    return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
    cart = Cart.objects.get(cart_id=_cart_id(request))  # lowercase cart as variable
    product = get_object_or_404(Product, id=product_id)
    cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
    try:
        cart_item.delete()
    except CartItem.DoesNotExist:
        pass  # Handle case where cart item doesn't exist
        
    return redirect('cart')

def cart(request, total=0, quantity=0, cart_items=None):
    try: 
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += cart_item.sub_total()  # Total calculation
            quantity += cart_item.quantity
        tax = (10 * total / 100)  # ✅ Fix tax calculation to 10% instead of 1%
        grand_total = total + tax
    except Cart.DoesNotExist:
        tax = 0
        grand_total = 0

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,  # ✅ Make sure tax is passed
        'grand_total': grand_total,  # ✅ Make sure grand_total is passed
    }

    return render(request, 'store/cart.html', context)

def checkout(request, total=0, quantity=0, cart_items=None):
    try: 
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        
        for cart_item in cart_items:
            total += cart_item.sub_total()  # Total calculation
            quantity += cart_item.quantity
        
        tax = (10 * total / 100)  # ✅ Set tax to 10%
        grand_total = total + tax

        # ✅ Debugging print statement
        print(f"Checkout - Total: {total}, Tax: {tax}, Grand Total: {grand_total}")

    except Cart.DoesNotExist:
        tax = 0
        grand_total = 0

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,  # ✅ Make sure tax is passed
        'grand_total': grand_total,  # ✅ Make sure grand_total is passed
    }

    return render(request, 'store/checkout.html', context)
