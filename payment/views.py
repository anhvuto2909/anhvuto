from django.shortcuts import render,redirect
from cart.cart import Cart
from payment.forms import ShippingForm, PaymentForm
from payment.models import ShippingAddress, Order, OrderItem
from django.contrib.auth.models import User
from django.contrib import messages
from store.models import Product

def process_order(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Get bill info from last page
        payment_form = PaymentForm(request.POST or None)
        # Get shipping session data
        my_shipping = request.session.get('my_shipping')
        # Gather Order Info
        full_name = my_shipping['shipping_full_name']
        email = my_shipping['shipping_email']

        shipping_address = f"{my_shipping['shipping_address1']}\n{my_shipping['shipping_address2']}\n{my_shipping['shipping_city']}\n{my_shipping['shipping_state']}\n{my_shipping['shipping_zipcode']}\n{my_shipping['shipping_country']}"
        amount_paid = totals


        if request.user.is_authenticated:
            user = request.user
            # create order
            create_order = Order(user = user, full_name = full_name, email = email, shipping_address = shipping_address, amount_paid = amount_paid)
            create_order.save()

            # Add order item 
            
            # Get the order ID

            order_id = create_order.pk 
            
            # Get the product info
            for product in cart_products():
                # Get the product ID
                product_id = product.id
                # Get product price 
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id = order_id ,product_id= product_id, user = user, quantity=value, price=price,)
                        create_order_item.save()

            messages.success(request, "Order Placed")
            return redirect('home')
        else:
            # Not login
            # create order
            create_order = Order(full_name = full_name, email = email, shipping_address = shipping_address, amount_paid = amount_paid)
            create_order.save()

             # Add order item 
            
            # Get the order ID

            order_id = create_order.pk 
            
            # Get the product info
            for product in cart_products():
                # Get the product ID
                product_id = product.id
                # Get product price 
                if product.is_sale:
                    price = product.sale_price
                else:
                    price = product.price

                # Get quantity
                for key, value in quantities().items():
                    if int(key) == product.id:
                        # Create order item
                        create_order_item = OrderItem(order_id = order_id ,product_id= product_id, quantity=value, price=price,)
                        create_order_item.save()




            messages.success(request, "Order Placed")
            return redirect('home')

    else:
        messages.success(request, "Access Denied")
        return redirect('home')
        



def billing_info(request):
    if request.POST:
        cart = Cart(request)
        cart_products = cart.get_prods
        quantities = cart.get_quants
        totals = cart.cart_total()

        # Create a session with shipping info 
        my_shipping = request.POST
        request.session['my_shipping'] = my_shipping

        if request.user.is_authenticated:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form":billing_form})
        else:
            billing_form = PaymentForm()
            return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities": quantities, "totals": totals, "shipping_info": request.POST, "billing_form":billing_form})

        shipping_form = request.POST
        return render(request, "payment/billing_info.html", {"cart_products":cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})
    else:
        messages.success(request, "Access Denied")
        return redirect('home')


def checkout(request):
    cart = Cart(request)
    cart_products = cart.get_prods
    quantities = cart.get_quants
    totals = cart.cart_total()

    if request.user.is_authenticated:
        # checkout as login
        shipping_user = ShippingAddress.objects.get(user__id = request.user.id)
        shipping_form = ShippingForm(request.POST or None, instance= shipping_user)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form })
    else:
        # checkout as guest
        shipping_form = ShippingForm(request.POST or None)
        return render(request, "payment/checkout.html", {"cart_products":cart_products, "quantities": quantities, "totals": totals, "shipping_form": shipping_form})    



def payment_success(request):   

    return render(request,"payment/payment_success.html", {})
