from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Review
        fields = ['id', 'user', 'username', 'book', 'rating', 'comment', 'created_at', 'updated_at']
        read_only_fields = ['user']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError('Baho 1 dan 5 gacha bo‘lishi kerak.')
        return value
