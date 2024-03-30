from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .admin import Book


class BookSerializers(serializers.ModelSerializer):

    class Meta:
        model = Book
        fields = ('id', 'title', 'content', 'subtitle', 'author', 'isbn', 'price')

    def validate(self, data):
        title = data.get('title', None)
        author = data.get('author', None)

        if not title.islpha():
            raise ValidationError(
                {
                    "status": False,
                    "message": "iltimos sarlavhani matn korinishida bering!"
                }
            )


        if Book.objects.filter(title=title, author=author).exists():
            raise ValidationError(
                {
                    "status": False,
                    "message": "sarlavha va muallif bir hil bolgan kitob yuklay olmaysiz!"
                }
            )

        return data

    def validate_price(self, attrs):
        if attrs<0 and attrs>999999999:
            raise ValidationError(
                {
                    "status": False,
                    "message": "narx notori kiritildi!"
                }
            )
