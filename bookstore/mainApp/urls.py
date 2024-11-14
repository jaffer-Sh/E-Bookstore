from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('books/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('books/create/', views.BookCreateView.as_view(), name='book_create'),
    path('books/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    path('books/<int:pk>/delete/', views.BookDeleteView.as_view(), name='book_delete'),
    path('add_book/', views.add_book, name='add_book'),
    path('books/<int:book_id>/add_review/', views.add_review, name='add_review'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('add_to_cart/<int:book_id>/', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart/<int:book_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('signup', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('add_address/', views.add_address, name='add_address'),
    path('choose_address/', views.choose_address, name='choose_address'),
    path('confirm_order/', views.confirm_order, name='confirm_order' ),
    path('confirm_payment/', views.confirm_payment, name='confirm_payment'),    
    path('select_address/<int:address_id>/', views.select_address, name='select_address'),
    path('checkout/', views.checkout, name='checkout'),
    path('order-history/', views.order_history, name='order_history'),

]


    