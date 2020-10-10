
from django.urls import path, include
from catalog import views 
urlpatterns = [
    path('', views.index, name='index'),
    path('books/', views.BookListView.as_view(), name='books'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book-detail'),
    path('authors/', views.AuthorListView.as_view(), name='authors'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author-detail'),
    path('mybooks/',views.LoanedBooksByUserListView.as_view(), name='my-books'),
    path('borrowed/',views.LoanedBookListView.as_view(), name='borrowed-books'),
    path('<uuid:instance_id>/return/', views.mark_book_returned, name='mark-returned'),
    path('<uuid:instance_id>/renew/', views.renew_book_librarian, name='renew-book-librarian'),
    #path('author/create/', views.AuthorCreate.as_view(), name='author-create'),
    #path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
    #path('author/<int:pk>/delete/', views.AuthorDelete.as_view(), name='author-delete'),
]
