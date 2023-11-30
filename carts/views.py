from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render,redirect
from store.models import Product,Variation
from .models import Cart, CartItem
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.
def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart
def add_cart(request,product_id):
    product = Product.objects.get(id=product_id)
    product_variantion = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            
            try:
                variation = Variation.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
                product_variantion.append(variation)
            except:
                pass
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id = _cart_id(request),
        )
    cart.save()
    is_cart_item_exists = CartItem.objects.filter(product=product,cart = cart).exists()
    if is_cart_item_exists:
        cart_item = CartItem.objects.filter(product = product,cart=cart)
        existing_variation_list = []
        id = []
        for item in cart_item:
            existing_variation = item.variation.all()
            existing_variation_list.append(list(existing_variation))
            id.append(item.id)
        if product_variantion in existing_variation_list:
            index = existing_variation_list.index(product_variantion)
            item_id = id[index]
            item = CartItem.objects.get(product=product, id=item_id)
            item.quantity += 1
            item.save()
        else:
            item = CartItem.objects.create(product=product, quantity = 1, cart = cart)
            if len(product_variantion)>0:
                item.variation.clear()
                item.variation.add(*product_variantion)
            item.save()
    else:
        cart_item = CartItem.objects.create(
            product = product,
            quantity = 1,
            cart = cart,
        )
        if len(product_variantion)>0:
            cart_item.variation.clear()
            cart_item.variation.add(*product_variantion)
        cart_item.save()
    return redirect('cart')

def remove_cart(request,product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product,id = product_id)
    try:
        cart_item = CartItem.objects.get(product=product,cart = cart, id = cart_item_id)
        if cart_item.quantity >1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except:
        pass
    return redirect('cart')

def remove_cart_item(request, product_id,cart_item_id):
    cart = Cart.objects.get(cart_id = _cart_id(request))
    product = get_object_or_404(Product, id = product_id)
    cart_item = CartItem.objects.get(product=product,cart = cart, id=cart_item_id)
    cart_item.delete()
    return redirect('cart')

def cart(request,total =0,quantity =0,cart_items=None):
    try:
        cart = Cart.objects.get(cart_id = _cart_id(request))
        cart_items = CartItem.objects.filter(cart = cart,is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.Price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (0.05 * total)
        tax = round(tax,2)

        grandtotal = total + tax
    except ObjectDoesNotExist:
        pass

    context = {
        'total': total ,
        'quantity': quantity ,
        'cart_items': cart_items ,
        'tax': tax,
        'grandtotal' : grandtotal,
    }
    return render(request, 'store/cart.html',context)