from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from rest_framework import generics, permissions
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializer
from reviews.models import Review


def home(request):
    books = Book.objects.order_by('-created_at')[:6]
    return render(request, 'home.html', {'books': books})


def book_list(request):
    books = Book.objects.all().annotate(avg_rating=Avg('reviews__rating'))
    search = request.GET.get('search', '').strip()
    author = request.GET.get('author', '').strip()
    year = request.GET.get('year', '').strip()
    if search:
        books = books.filter(Q(title__icontains=search))
    if author:
        books = books.filter(author__icontains=author)
    if year.isdigit():
        books = books.filter(published_date__year=year)
    return render(request, 'books/list.html', {'books': books, 'search': search, 'author': author, 'year': year})


def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    reviews = book.reviews.select_related('user').all()
    avg_rating = reviews.aggregate(avg=Avg('rating'))['avg']
    my_review = reviews.filter(user=request.user).first() if request.user.is_authenticated else None
    return render(request, 'books/detail.html', {
        'book': book,
        'reviews': reviews,
        'avg_rating': round(avg_rating, 1) if avg_rating else 0,
        'my_review': my_review,
    })


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or request.user.role == 'admin')


class BookViewSet(ModelViewSet):
    queryset = Book.objects.all().order_by('-created_at')
    serializer_class = BookSerializer

    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [permissions.AllowAny()]
        return [IsAdmin()]
