from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from book.models import Book
from reviews.models import Review


def is_admin(user):
    return user.is_authenticated and (user.is_staff or user.role == 'admin')


admin_required = user_passes_test(is_admin, login_url='/users/login/')


@admin_required
def dashboard(request):
    return render(request, 'admin_dashboard/dashboard.html', {
        'book_count': Book.objects.count(),
        'review_count': Review.objects.count(),
    })


@admin_required
def books(request):
    return render(request, 'admin_dashboard/books.html', {'books': Book.objects.all().order_by('-created_at')})


@admin_required
def book_add(request):
    if request.method == 'POST':
        Book.objects.create(
            title=request.POST.get('title'), author=request.POST.get('author'),
            description=request.POST.get('description'), published_date=request.POST.get('published_date') or None,
            cover_image=request.FILES.get('cover_image'),
        )
        messages.success(request, 'Kitob qo‘shildi.')
        return redirect('dashboard_books')
    return render(request, 'admin_dashboard/book_form.html', {'book': None})


@admin_required
def book_edit(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.title = request.POST.get('title')
        book.author = request.POST.get('author')
        book.description = request.POST.get('description')
        book.published_date = request.POST.get('published_date') or None
        if request.FILES.get('cover_image'):
            book.cover_image = request.FILES['cover_image']
        book.save()
        messages.success(request, 'Kitob yangilandi.')
        return redirect('dashboard_books')
    return render(request, 'admin_dashboard/book_form.html', {'book': book})


@admin_required
def book_delete(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if request.method == 'POST':
        book.delete()
        messages.success(request, 'Kitob o‘chirildi.')
    return redirect('dashboard_books')


@admin_required
def reviews(request):
    return render(request, 'admin_dashboard/reviews.html', {'reviews': Review.objects.select_related('user', 'book').all()})



@admin_required
def review_edit(request, pk):
    review = get_object_or_404(Review, pk=pk)
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
            return redirect('dashboard_reviews')
        messages.error(request, 'Baho 1-5 oralig‘ida bo‘lishi va izoh yozilishi kerak.')
    return render(request, 'admin_dashboard/review_form.html', {'review': review})

@admin_required
def review_delete(request, pk):
    review = get_object_or_404(Review, pk=pk)
    if request.method == 'POST':
        review.delete()
        messages.success(request, 'Sharh o‘chirildi.')
    return redirect('dashboard_reviews')
