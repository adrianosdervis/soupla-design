from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from shop.models import Customer, ContactDetail, InvoiceDetail, Order
from .forms import UserRegisterForm
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist


def login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user is not None:
                auth.login(request, user)
                messages.success(request, f'Welcome, {username}!')
                return redirect('shop')
            else:
                messages.error(request, 'Invalid credentials')
                return redirect('login')
        else:
            return render(request, 'accounts/login.html')
    else:
        messages.info(request, 'You are already logged in')
        return redirect('shop')


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('email')
            if User.objects.filter(email=email).exists():
                messages.error(request, f'Email "{email}" is used.')
                return redirect('register')

            form.save()

            username = form.cleaned_data.get('username')

            customer_user = User.objects.get(username=username)
            first_name = form.cleaned_data.get('first_name')
            last_name = form.cleaned_data.get('last_name')
            customer = Customer(
                user=customer_user, name=f'{first_name} {last_name}', email=email)
            customer.save()

            messages.success(
                request, f'{username}, your account has been created! Please login.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


# def logout(request):
#     if request.method == 'POST':
#         auth.logout(request)
#         messages.info(request, 'You are logged out.')
#         return redirect('shop')
#     else:
#         return redirect('shop')


def logout(request):
    auth.logout(request)
    messages.info(request, 'You are logged out.')
    return redirect('shop')


@login_required
def profile(request):
    customer = request.user.customer
    try:
        orders = Order.objects.all().filter(customer=customer, complete=True)
    except ObjectDoesNotExist:
        orders = None
    try:
        order = Order.objects.get(customer=customer, complete=False)
        cartItems = order.get_cart_items
    except ObjectDoesNotExist:
        order = None
        cartItems = None
    try:
        contactDetails = ContactDetail.objects.get(customer=customer)
    except ObjectDoesNotExist:
        contactDetails = None
    try:
        invoiceDetails = InvoiceDetail.objects.get(customer=customer)
    except ObjectDoesNotExist:
        invoiceDetails = None

    if request.method == 'POST':
        responsibleName = request.POST['responsible-name']
        landline = request.POST['landline']
        mobile = request.POST['mobile']
        email = request.POST['email']
        brand = request.POST['brand']
        brandDescription = request.POST['brand-activity']
        afm = request.POST['afm']
        taxOffice = request.POST['tax-office']
        brandAddress = request.POST['brand-address']
        brandAddress2 = request.POST['brand-address2']
        invoice_zipcode = request.POST['invoice-po-box']

        contactDetails, created = ContactDetail.objects.update_or_create(customer=customer, defaults={
            'responsible_name': responsibleName,
            'landline': landline,
            'mobile': mobile,
            'email': email
        })
        contactDetails.save()
        invoiceDetails, created = InvoiceDetail.objects.update_or_create(customer=customer, defaults={
            'brand': brand,
            'brand_description': brandDescription,
            'afm': afm,
            'tax_office': taxOffice,
            'address1': brandAddress,
            'address2': brandAddress2,
            'zipcode': invoice_zipcode,
        })
        invoiceDetails.save()

        messages.success(request, 'Οι αλλαγές σας αποθηκεύτηκαν!')

    context = {
        'customer': customer,
        'orders': orders,
        'cartItems': cartItems,
        'contactDetails': contactDetails,
        'invoiceDetails': invoiceDetails,
    }

    return render(request, 'accounts/profile.html', context)
