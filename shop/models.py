from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Packet(models.Model):
    packet_number = models.PositiveIntegerField()
    price = models.FloatField()

    class Meta:
        ordering = ('packet_number', 'price',)
        verbose_name = 'packet'
        verbose_name_plural = 'packet'

    def __str__(self):
        return f'{str(self.packet_number)} - {str(self.price)}€'


class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    thumbnail = models.ImageField(
        null=True, blank=True, upload_to='product', default='placeholder.png')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    packets = models.ManyToManyField(Packet)

    class Meta:
        ordering = ('id',)
        verbose_name = 'product'
        verbose_name_plural = 'products'

    def get_url(self):
        return reverse('product', args=[self.id])

    def __str__(self):
        return self.name


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name


class ContactDetail(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    responsible_name = models.CharField(max_length=200)
    landline = models.CharField(max_length=20, blank=True)
    mobile = models.CharField(max_length=20)
    email = models.EmailField(max_length=254, null=True, blank=True)

    class Meta:
        ordering = ('customer',)

    def __str__(self):
        return self.responsible_name


class Order(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    date_ordered = models.DateTimeField(auto_now=True)
    complete = models.BooleanField(default=False)
    bank_transaction_id = models.CharField(max_length=100)
    notes = models.TextField(blank=True)  # new

    class Meta:
        ordering = ('date_ordered',)

    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    def __str__(self):
        return str(self.id)


class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    packet = models.PositiveIntegerField(null=True)
    price = models.FloatField(null=True)
    quantity = models.PositiveSmallIntegerField(default=0)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('order',)

    @property
    def get_total(self):
        total = self.price * self.quantity
        return total

    def __str__(self):
        return self.product.name


class InvoiceDetail(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    brand = models.CharField(max_length=250)
    brand_description = models.CharField(max_length=500)
    afm = models.CharField(max_length=9, blank=True)
    tax_office = models.CharField(max_length=100)
    address1 = models.CharField(max_length=500)
    address2 = models.CharField(max_length=500)
    zipcode = models.CharField(max_length=200)  # new
    date_added = models.DateTimeField(auto_now_add=True)  # new

    class Meta:
        ordering = ('brand',)

    def __str__(self):
        return self.brand


class ShippingAddress(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    shipping_name = models.CharField(max_length=250, blank=True)
    address1 = models.CharField(max_length=500, blank=True)
    address2 = models.CharField(max_length=500, blank=True)
    zipcode = models.CharField(max_length=200, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'shipping addresses'
        ordering = ('shipping_name',)

    def __str__(self):
        return self.address
