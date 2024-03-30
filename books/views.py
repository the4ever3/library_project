from django.shortcuts import render, get_object_or_404
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Book
from .serializers import BookSerializers
from rest_framework import generics, status, viewsets


# class BookListApiView(generics.ListAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers

class BookListApiView(APIView):

    def get(self, request):
        books = Book.objects.all()
        serializer_data = BookSerializers(books, many=True).data
        data = {
            "status": f"returned {len(books)} books.",
            "books": serializer_data,
        }
        return Response(data)


# class BookDetailApiView(generics.RetrieveAPIView):
#     queryset = Book.objects.all()
#     serializer_class =  BookSerializers

class BookDetailApiView(APIView):
    def get(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            serializer_data = BookSerializers(book).data

            data = {
                'status': "Succsessfull",
                "book": serializer_data
            }
            return Response(data, status=status.HTTP_200_OK)
        except Exception:
            return Response(
                {
                    "status": False,
                    "message": "Book is not found"
                },
                status=status.HTTP_404_NOT_FOUND
            )



# class BookDeleteApiView(generics.DestroyAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers

class BookDeleteApiView(APIView):

    def delete(self, request, pk):
        try:
            book = Book.objects.get(id=pk)
            book.delete()
            return Response(
                {
                    "status": True,
                    "message": "Successfull deleted"
                },
                status=status.HTTP_200_OK
            )
        except Exception:
            return Response(
                {
                    "status": False,
                    "message": "failed"
                },
                status=status.HTTP_400_BAD_REQUEST
            )


# class BookUpdateApiView(generics.UpdateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers

class BookUpdateApiView(APIView):
    def put(self, request, pk):
        book = get_object_or_404(Book.objects.all(), id=pk)
        data = request.data
        serializer = BookSerializers(instance=book, data=data, partial=True)
        if serializer.is_valid(raise_exception=True):
            book_saved = serializer.save()
        return Response(
            {
                "status": True,
                "message": f"Book {book_saved} seccessfull updated"
            }
        )



# class BookCreateApiView(generics.CreateAPIView):
#     queryset = Book.objects.all()
#     serializer_class = BookSerializers

class BookCreateApiView(APIView):

    def post(self, request):
        data = request.data
        serializer = BookSerializers(data=data)
        if serializer.is_valid(raise_exception=True):
            books = serializer.save()
            data = {'status': f"Books are created to the database",
                    'books': data
                    }
            return Response(data)


class BookListCreateApiView(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers




class BookUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


class BookViewset(ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


@api_view((['GET']))
def book_list_view(request, *args, **kwargs):
    books = Book.objects.all()
    serializers = BookSerializers(books, many=True)
    return Response(serializers.data)
