from django.urls import path
from .views import book_add, book_delete, book_edit, books, dashboard, review_delete, review_edit, reviews

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('books/', books, name='dashboard_books'),
    path('books/add/', book_add, name='dashboard_book_add'),
    path('books/<int:pk>/edit/', book_edit, name='dashboard_book_edit'),
    path('books/<int:pk>/delete/', book_delete, name='dashboard_book_delete'),
    path('reviews/', reviews, name='dashboard_reviews'),
    path('reviews/<int:pk>/edit/', review_edit, name='dashboard_review_edit'),
    path('reviews/<int:pk>/delete/', review_delete, name='dashboard_review_delete'),
]
