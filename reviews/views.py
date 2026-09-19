from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from rest_framework import generics, permissions
from rest_framework.exceptions import PermissionDenied
from rest_framework.viewsets import ModelViewSet

from book.models import Book
from .models import Review
from .serializers import ReviewSerializer


@login_required
def add_review(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    if request.method == 'POST':
        if Review.objects.filter(user=request.user, book=book).exists():
            messages.error(request, 'Siz bu kitobga allaqachon sharh yozgansiz.')
        else:
            rating = request.POST.get('rating')
            comment = request.POST.get('comment', '').strip()
            try:
                rating = int(rating)
            except (TypeError, ValueError):
                rating = 0
            if 1 <= rating <= 5 and comment:
                Review.objects.create(user=request.user, book=book, rating=rating, comment=comment)
                messages.success(request, 'Sharhingiz qo‘shildi.')
            else:
                messages.error(request, 'Baho 1-5 oralig‘ida bo‘lishi va izoh yozilishi kerak.')
    return redirect('book_detail', pk=book.id)



@login_required
def edit_my_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.user != request.user:
        raise PermissionDenied
    if request.method == 'POST':
        try:
            rating = int(request.POST.get('rating'))
        except (TypeError, ValueError):
            rating = 0
        comment = request.POST.get('comment', '').strip()
        if 1 <= rating <= 5 and comment:
            review.rating = rating
            review.comment = comment
            review.save()
            messages.success(request, 'Sharh yangilandi.')
            return redirect('book_detail', pk=review.book_id)
        messages.error(request, 'Baho 1-5 oralig‘ida bo‘lishi va izoh yozilishi kerak.')
    return __import__('django.shortcuts', fromlist=['render']).render(request, 'reviews/edit.html', {'review': review})

@login_required
def delete_my_review(request, review_id):
    review = get_object_or_404(Review, pk=review_id)
    if review.user != request.user:
        raise PermissionDenied
    review.delete()
    messages.success(request, 'Sharh o‘chirildi.')
    return redirect('book_detail', pk=review.book_id)


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and (request.user.is_staff or getattr(request.user, 'role', '') == 'admin')


class ReviewListAPIView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return Review.objects.select_related('user', 'book').all()


class BookReviewListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(book_id=self.kwargs['book_id']).select_related('user')

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    def perform_create(self, serializer):
        book = get_object_or_404(Book, pk=self.kwargs['book_id'])
        if Review.objects.filter(user=self.request.user, book=book).exists():
            from rest_framework.exceptions import ValidationError
            raise ValidationError('Siz bu kitobga allaqachon sharh yozgansiz.')
        serializer.save(user=self.request.user, book=book)


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.select_related('user', 'book').all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAdmin()]
        return [permissions.IsAuthenticated()]

    def perform_update(self, serializer):
        if not (self.request.user.is_staff or self.request.user.role == 'admin') and serializer.instance.user != self.request.user:
            raise PermissionDenied('Faqat o‘zingizning sharhingizni o‘zgartira olasiz.')
        serializer.save()

    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or self.request.user.role == 'admin') and instance.user != self.request.user:
            raise PermissionDenied('Faqat o‘zingizning sharhingizni o‘chira olasiz.')
        instance.delete()
