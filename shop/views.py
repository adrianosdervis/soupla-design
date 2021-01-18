from django.shortcuts import render, redirect
from .models import *
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.contrib import messages
import json
from django.core.exceptions import ObjectDoesNotExist

from django.core.mail import EmailMessage
from django.conf import settings
from django.template.loader import get_template


def shop(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        # items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        cartItems = None

    products = Product.objects.all()
    # Pagination #
    page = request.GET.get('page')
    paginator = Paginator(products, 9)
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)
    # Pagination #
    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'shop/home.html', context)


def product(request, pk):
    product = Product.objects.get(id=pk)
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        cartItems = order.get_cart_items
        context = {'product': product, 'cartItems': cartItems}
    else:
        context = {'product': product}
    return render(request, 'shop/product.html', context)


def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all().order_by('product', 'price')
        cartItems = order.get_cart_items
    else:
        return redirect('login')

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'shop/cart.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    packet = data['packet']
    price = data['price']

    customer = request.user.customer
    product = Product.objects.get(id=productId)

    order, created = Order.objects.get_or_create(
        customer=customer, complete=False)
    orderItem, created = OrderItem.objects.get_or_create(
        order=order, product=product, packet=packet, price=price)

    orderItem.packet = packet
    orderItem.price = price

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1

    orderItem.save()

    if orderItem.quantity <= 0 or action == 'delete':
        orderItem.delete()

    return JsonResponse({
        'cart_items': order.get_cart_items,
        'cart_total': order.get_cart_total
    }, safe=False)


def orderInfo(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(
            customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
        try:
            contactDetails = ContactDetail.objects.get(customer=customer)
        except ObjectDoesNotExist:
            contactDetails = None
        try:
            invoiceDetails = InvoiceDetail.objects.get(customer=customer)
        except ObjectDoesNotExist:
            invoiceDetails = None
    else:
        return redirect('login')

    context = {'items': items,
               'order': order,
               'cartItems': cartItems,
               'contactDetails': contactDetails,
               'invoiceDetails': invoiceDetails
               }
    return render(request, 'shop/order_info.html', context)


def sendOrder(request):
    if request.user.is_authenticated:
        if request.method == 'POST':

            customer = request.user.customer
            order, created = Order.objects.get_or_create(
                customer=customer, complete=False)
            items = order.orderitem_set.all()

            #### GET THE VALUES FROM THE FORM ####
            # Contact details
            responsible_name = request.POST['responsible-name']
            landline = request.POST['landline']
            mobile = request.POST['mobile']
            email = request.POST['email']

            # Invoice details
            brand = request.POST['brand']
            brand_activity = request.POST['brand-activity']
            afm = request.POST['afm']
            tax_office = request.POST['tax-office']
            brand_address = request.POST['brand-address']
            brand_address2 = request.POST['brand-address2']
            invoice_zipcode = request.POST['invoice-po-box']
            is_checked = request.POST['is_checked']

            # Shipping details
            shipping_name = request.POST['shipping-name']
            shipping_address = request.POST['shipping-address']
            shipping_address2 = request.POST['shipping-address2']
            po_box = request.POST['po-box']

            # For the order
            bank_id = request.POST['bank-id']
            order_notes = request.POST['order-notes']

            file1 = request.FILES.get('file1', False)
            file2 = request.FILES.get('file2', False)

            isPDForTIFF = ((True if file1.name.endswith('.pdf') else False) or (True if file1.name.endswith('.tiff') else False) or (True if file1.name.endswith('.zip') else False) or (True if file1.name.endswith('.rar') else False) or (True if file1.name.endswith('.jpg') else False) or (True if file1.name.endswith('.jpeg') else False)) and (
                (True if file2.name.endswith('.pdf') else False) or (True if file2.name.endswith('.tiff') else False) or (True if file2.name.endswith('.zip') else False) or (True if file2.name.endswith('.rar') else False) or (True if file2.name.endswith('.jpg') else False) or (True if file2.name.endswith('.jpeg') else False))

            isLarge = (True if file1.size + file2.size > 60000000 else False)

            if isLarge:
                messages.error(
                    request, 'Τα αρχεία πρέπει να είναι μέχρι 60ΜΒ σύνολο')
                return redirect('order_info')

            if not isPDForTIFF:
                messages.error(
                    request, 'Τα αρχεία πρέπει να είναι .pdf, .tiff, .jpg, .zip, .rar')
                return redirect('order_info')

            #### SAVE ORDER ####
            order, created = Order.objects.update_or_create(customer=customer, complete=False, defaults={
                'complete': True,
                'bank_transaction_id': bank_id,
                'notes': order_notes
            })
            order.save()

            #### SAVE CONTACT DETAILS ####
            contactDetails, created = ContactDetail.objects.get_or_create(
                customer=customer)
            contactDetails, created = ContactDetail.objects.update_or_create(customer=customer, defaults={
                'responsible_name': responsible_name,
                'landline': landline,
                'mobile': mobile,
                'email': email
            })
            contactDetails.save()

            #### SAVE INVOICE DETAILS ####
            invoiceDetails, created = InvoiceDetail.objects.get_or_create(
                customer=customer)
            invoiceDetails, created = InvoiceDetail.objects.update_or_create(customer=customer, defaults={
                'brand': brand,
                'brand_description': brand_activity,
                'afm': afm,
                'tax_office': tax_office,
                'address1': brand_address,
                'address2': brand_address2,
                'zipcode': invoice_zipcode,
            })
            invoiceDetails.save()

            #### SAVE SHIPPING DETAILS ####
            shippingDetails, created = ShippingAddress.objects.get_or_create(
                customer=customer)
            if is_checked == 'checked':
                shippingDetails, created = ShippingAddress.objects.update_or_create(customer=customer, defaults={
                    'order': order,
                    'shipping_name': brand,
                    'address1': brand_address,
                    'address2': brand_address2,
                    'zipcode': invoice_zipcode,
                })
                shippingDetails.save()
            elif is_checked == 'unchecked':
                shippingDetails, created = ShippingAddress.objects.update_or_create(customer=customer, defaults={
                    'order': order,
                    'shipping_name': shipping_name,
                    'address1': shipping_address,
                    'address2': shipping_address2,
                    'zipcode': po_box,
                })
                shippingDetails.save()

            context = {
                'order': order,
            }

            # data for email
            msg_information = {
                'order': order,
                'contactDetails': contactDetails,
                'invoiceDetails': invoiceDetails,
                'shippingDetails': shippingDetails,
                'items': items,
            }
            message = get_template(
                'shop/email_msg_template.html').render(msg_information)
            msg = EmailMessage(
                'Νέα παραγγελία',
                message,
                from_email=settings.EMAIL_HOST_USER,
                to=[settings.EMAIL_HOST_USER, email]
            )
            msg.content_subtype = 'html'
            msg.fail_silently = False
            msg.attach(file1.name, file1.read(), file1.content_type)
            msg.attach(file2.name, file2.read(), file2.content_type)
            msg.send()
            # -----------------------------------------------

            return render(request, 'shop/thanks.html', context)
    else:
        return redirect('login')
