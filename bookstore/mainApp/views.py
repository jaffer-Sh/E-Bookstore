from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from .models import Book, Review, CartItem, Order, Address
from .forms import ReviewForm, AddressForm, BookForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages


def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'
    context_object_name = 'books'

class BookDetailView(DetailView):
    model = Book
    template_name = 'books/book_detail.html'

class BookCreateView(LoginRequiredMixin, CreateView):
    model = Book
    fields = ['title', 'author', 'category', 'rating', 'price', 'image']
    template_name = 'books/book_form.html'

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = Book
    fields = ['title', 'author', 'category', 'rating', 'price', 'image']
    template_name = 'books/book_form.html'

class BookDeleteView(LoginRequiredMixin, DeleteView):
    model = Book
    template_name = 'books/book_confirm_delete.html'
    success_url = reverse_lazy('book_list')

@login_required
def add_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            book = form.save(commit=False)
            book.user = request.user  # Assuming you want to associate the book with the user
            book.save()
            return redirect('book_list')  # Redirect to the book list page
    else:
        form = BookForm()
    return render(request, 'books/add_book.html', {'form': form})

@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=book_id)
    else:
        form = ReviewForm()
    return render(request, 'books/add_review.html', {'form': form, 'book': book})


@login_required
def add_to_cart(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = CartItem.objects.get_or_create(book=book, defaults={'quantity': 1})
    if not created:
        cart_item.quantity += 1
    cart_item.save()
    return redirect('cart_detail')

@login_required
def cart_detail(request):
    cart_items = CartItem.objects.all()
    cart_data = []
    total = 0
    for item in cart_items:
        item_total = item.book.price * item.quantity
        cart_data.append({'item': item, 'item_total': item_total})
        total += item_total
    return render(request, 'books/cart_detail.html', {'cart_data': cart_data, 'total': total})

@login_required
def remove_from_cart(request, book_id):
    cart_item = get_object_or_404(CartItem, book_id=book_id)
    cart_item.delete()
    return redirect('cart_detail')

def signup(request):
  error_message = ''
  if request.method == 'POST':
    form = UserCreationForm(request.POST)
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid Sign Up - Please try again later.'

  form = UserCreationForm()
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)

def choose_address(request):
    if request.method == 'POST':
        address_id = request.POST.get('address_id')
        order = Order.objects.create(
            user=request.user,
            delivery_option='delivery',
            address=Address.objects.get(id=address_id)
        )
        return redirect('payment_page', order_id=order.id)
    else:
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'books/choose_address.html', {'addresses': addresses})


@login_required
def select_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)   
    order = Order.objects.filter(user=request.user, address__isnull=True).first()

    if order:
        order.address = address
        order.save()
        
    return redirect('confirm_order')



@login_required
def confirm_order(request):
    order = Order.objects.filter(user=request.user).last()

    if not order:
        messages.error(request, "Order not found.")
        return redirect('checkout')

    delivery_option = order.delivery_option
    # Fetch addresses only if delivery option is set to "delivery"
    addresses = Address.objects.filter(user=request.user) if delivery_option == 'delivery' else []

    return render(request, 'books/confirm_order.html', {
        'total_cost': order.total_cost,
        'delivery_option': delivery_option,
        'addresses': addresses,
        'order': order
    })

@login_required
def select_address(request, address_id):
    address = get_object_or_404(Address, id=address_id)   
    order = Order.objects.filter(user=request.user, address__isnull=True).first()

    if order:
        order.address = address
        order.save()

@login_required
def confirm_payment(request):
    order = Order.objects.filter(user=request.user).last()

    if not order:
        messages.error(request, "Order not found.")
        return redirect('checkout')
    
    return render(request, 'books/checkout.html', {
        'order': order,
        'total_cost': order.total_cost,
        'address': order.address,
    })
    
@login_required
def checkout(request):
    cart_items = CartItem.objects.all()
    total_cost = sum(item.book.price * item.quantity for item in cart_items)
    
    if request.method == "POST":
        delivery_option = request.POST.get('delivery_option')
        address_id = request.POST.get('address_id')
        
        if delivery_option == 'delivery' and not address_id:
            messages.error(request, "Please select a delivery address.")
            return redirect('checkout')

        address = Address.objects.get(id=address_id) if delivery_option == 'delivery' else None
        order = Order.objects.create(
            user=request.user,
            delivery_option=delivery_option,
            address=address,
            total_cost=total_cost
        )
        order.items.set(cart_items)
        
        CartItem.objects.all().delete()
        messages.success(request, "The order has been successfully confirmed!")
        return redirect('order_history')

    addresses = Address.objects.filter(user=request.user)
    return render(request, 'books/checkout.html', {
        'cart_items': cart_items,
        'total_cost': total_cost,
        'addresses': addresses,
    })
    
@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, 'books/order_history.html', {'orders': orders})

@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            address = form.save(commit=False)
            address.user = request.user
            address.save()
            return redirect('choose_address')
    else:
        form = AddressForm()
    return render(request, 'books/add_address.html', {'form': form})

# def book_list(request):
#     books = Book.objects.all()
#     return render(request, 'books/book_list.html', {'books': books})

# def book_detail(request, book_id):
#     book = get_object_or_404(Book, id=book_id)
#     return render(request, 'books/book_detail.html', {'book': book})