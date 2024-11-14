from django.contrib import admin
from .models import Book, Review, CartItem, Order, Address

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(Address)