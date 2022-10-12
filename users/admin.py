from django.contrib import admin
from .models import Profile, Product, Order
from django.contrib.auth.models import Group

admin.site.site_header = 'e-TAKA Dashboard'


class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'quantity', 'category')
    list_filter = ['category']


# Register your models here.

admin.site.register(Product, ProductAdmin)
admin.site.register(Order)
admin.site.register(Profile)
