from django.contrib import admin
from .models import Product, Salesperson, Customer, Sales, Discount

admin.site.register(Product)
admin.site.register(Salesperson)
admin.site.register(Customer)
admin.site.register(Sales)
admin.site.register(Discount)