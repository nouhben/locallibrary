
from django.urls import path, include
from catalog.views import index, BookListView, BookDetailView, AuthorDetailView, AuthorListView
urlpatterns = [
    path('', index, name='index'),
    path('books/', BookListView.as_view(), name='books'),
    path('book/<int:pk>/', BookDetailView.as_view(), name='book-detail'),
    path('authors/', AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', AuthorDetailView.as_view(), name='author-detail'),
    # path('catalog/books/')
    # path('catalog/authors/')
    # path('catalog/book/<id>/')
    # path('catalog/author/<id>/')
    # path('catalog/books/')
]
