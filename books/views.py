from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.utils import timezone
from datetime import timedelta
from .models import Book, Category, BookBorrowing, BookRating
from unidecode import unidecode

def home(request):
    return render(request, 'books/home.html')

def book_list(request):
    categories = Category.objects.all()
    category_id = request.GET.get('category')
    books = Book.objects.all()
    
    if category_id:
        books = books.filter(category_id=category_id)
    
    return render(request, 'books/book_list.html', {
        'books': books,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })

def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    user_rating = None
    if request.user.is_authenticated:
        user_rating = BookRating.objects.filter(book=book, user=request.user).first()
    return render(request, 'books/book_detail.html', {
        'book': book,
        'user_rating': user_rating
    })

@login_required
def borrow_book(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.available_copies > 0:
        BookBorrowing.objects.create(
            user=request.user,
            book=book,
            borrow_date=timezone.now()
        )
        book.available_copies -= 1
        book.save()
        messages.success(request, f'You have successfully borrowed {book.title}')
    else:
        messages.error(request, 'This book is not available for borrowing')
    return redirect('books:book_detail', pk=pk)

@login_required
def return_book(request, pk):
    borrowing = get_object_or_404(
        BookBorrowing,
        book_id=pk,
        user=request.user,
        is_returned=False
    )
    borrowing.is_returned = True
    borrowing.return_date = timezone.now()
    borrowing.save()
    
    book = borrowing.book
    book.available_copies += 1
    book.save()
    
    messages.success(request, f'You have successfully returned {book.title}')
    return redirect('books:book_detail', pk=pk)

@login_required
def rate_book(request, pk):
    if request.method == 'POST':
        book = get_object_or_404(Book, pk=pk)
        rating = request.POST.get('rating')
        comment = request.POST.get('comment', '')
        
        if rating:
            BookRating.objects.update_or_create(
                user=request.user,
                book=book,
                defaults={'rating': rating, 'comment': comment}
            )
            messages.success(request, 'Your rating has been saved')
        else:
            messages.error(request, 'Please provide a rating')
    return redirect('books:book_detail', pk=pk)

def category_books(request, pk):
    category = get_object_or_404(Category, pk=pk)
    books = Book.objects.filter(category=category)
    return render(request, 'books/category_books.html', {
        'category': category,
        'books': books
    })

def search_books(request):
    query = request.GET.get('q', '').strip()
    category_id = request.GET.get('category')
    
    print(f"Original search query: '{query}'")
    print(f"Search query encoded: {query.encode('utf-8')}")
    
    books = Book.objects.all()
    print(f"Total books before filter: {books.count()}")
    
    if query:
        # Get all books and filter in Python to debug the matching
        all_books = list(books)
        matched_books = []
        
        for book in all_books:
            print(f"\nChecking book: {book.title}")
            print(f"Book title encoded: {book.title.encode('utf-8')}")
            
            # Convert both to lowercase for case-insensitive comparison
            book_title_lower = book.title.lower()
            query_lower = query.lower()
            
            print(f"Lowercase comparison - Book: '{book_title_lower}', Query: '{query_lower}'")
            
            # Check if query is in book title
            if query_lower in book_title_lower:
                print(f"Match found! Query '{query_lower}' is in '{book_title_lower}'")
                matched_books.append(book)
                continue
            
            # Try with ASCII conversion
            ascii_title = unidecode(book_title_lower)
            ascii_query = unidecode(query_lower)
            
            print(f"ASCII comparison - Book: '{ascii_title}', Query: '{ascii_query}'")
            
            if ascii_query in ascii_title:
                print(f"ASCII match found! Query '{ascii_query}' is in '{ascii_title}'")
                matched_books.append(book)
        
        # Convert matched books back to queryset
        if matched_books:
            books = Book.objects.filter(id__in=[book.id for book in matched_books])
        else:
            books = Book.objects.none()
        
        print(f"\nTotal books after filter: {books.count()}")
        print(f"Found books: {[book.title for book in books]}")
    
    if category_id:
        books = books.filter(category_id=category_id)
    
    categories = Category.objects.all()
    
    return render(request, 'books/search_results.html', {
        'books': books,
        'query': query,
        'categories': categories,
        'selected_category': int(category_id) if category_id else None
    })
