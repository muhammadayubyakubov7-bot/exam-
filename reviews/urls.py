from django.urls import path
from .views import add_review, delete_my_review, edit_my_review

urlpatterns = [
    path('book/<int:book_id>/add/', add_review, name='add_review'),
    path('<int:review_id>/edit/', edit_my_review, name='edit_my_review'),
    path('<int:review_id>/delete/', delete_my_review, name='delete_my_review'),
]
