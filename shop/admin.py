from django.contrib import admin
from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'created', 'updated']
    list_per_page = 20
    filter_horizontal = ['packets']


admin.site.register(Product, ProductAdmin)


class PacketAdmin(admin.ModelAdmin):
    list_display = ['packet_number', 'price']
    list_per_page = 20


admin.site.register(Packet, PacketAdmin)


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['name', 'user', 'email']
    list_per_page = 20


admin.site.register(Customer, CustomerAdmin)


class ContactDetailAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['customer', 'responsible_name',
                    'landline', 'mobile', 'email']


admin.site.register(ContactDetail, ContactDetailAdmin)


class InvoiceDetailAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['brand', 'customer', 'brand_description']


admin.site.register(InvoiceDetail, InvoiceDetailAdmin)


class OrderAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['id', 'customer', 'date_ordered',
                    'complete', 'bank_transaction_id']
    list_editable = ['complete']
    list_filter = ('complete',)


admin.site.register(Order, OrderAdmin)


class OrderItemAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['order', 'product', 'packet', 'price', 'quantity', ]
    list_display_links = ['order', 'product']
    list_filter = ('order',)


admin.site.register(OrderItem, OrderItemAdmin)


class ShippingAddressAdmin(admin.ModelAdmin):
    list_per_page = 20
    list_display = ['shipping_name', 'address1',
                    'zipcode', 'order', 'customer']


admin.site.register(ShippingAddress, ShippingAddressAdmin)
