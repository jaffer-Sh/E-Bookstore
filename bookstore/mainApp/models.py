from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    image = models.ImageField(upload_to='main_app/static/images', default="")
    

    def _str_(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'pk': self.id})

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='reviews')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField()
    comment = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    def _str_(self):
        return f"Review {self.rating} for {self.book.title}"

 
class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    address_line = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)

    def _str_(self):
        return f"{self.address_line}, {self.city}"

class CartItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(CartItem)
    delivery_option = models.CharField(max_length=20, choices=[('branch', 'Branch Pickup'), ('delivery', 'Delivery')])
    address = models.ForeignKey(Address, null=True, blank=True, on_delete=models.SET_NULL)
    total_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)

    def calculate_total_cost(self):
        return sum(item.book.price * item.quantity for item in self.items.all()) 
