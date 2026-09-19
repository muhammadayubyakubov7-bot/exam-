from django.db.models import Avg
from rest_framework import serializers

from .models import Book


class BookSerializer(serializers.ModelSerializer):
    avg_rating = serializers.SerializerMethodField()

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'description', 'cover_image', 'published_date', 'avg_rating', 'created_at']

    def get_avg_rating(self, obj):
        value = obj.reviews.aggregate(avg=Avg('rating'))['avg']
        return round(value, 1) if value is not None else 0
