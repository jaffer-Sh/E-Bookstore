from django import forms
from .models import Review, Address, Book

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['address_line', 'city', 'postal_code']
        
class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author', 'category', 'rating', 'price', 'image']    