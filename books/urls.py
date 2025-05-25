from django.urls import path
from . import views

app_name = 'books'

urlpatterns = [
    path('', views.home, name='home'),
    path('books/', views.book_list, name='book_list'),
    path('books/<int:pk>/', views.book_detail, name='book_detail'),
    path('books/<int:pk>/borrow/', views.borrow_book, name='borrow_book'),
    path('books/<int:pk>/return/', views.return_book, name='return_book'),
    path('books/<int:pk>/rate/', views.rate_book, name='rate_book'),
    path('categories/<int:pk>/', views.category_books, name='category_books'),
    path('search/', views.search_books, name='search_books'),
] 