
from django.urls import path, include
from catalog.views import index, BookListView, BookDetailView
urlpatterns = [
    path('', index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail')
    # path('catalog/books/')
    # path('catalog/authors/')
    # path('catalog/book/<id>/')
    # path('catalog/author/<id>/')
    # path('catalog/books/')
]
