
from django.urls import path, include
from catalog.views import index
urlpatterns = [
    path('', index, name='index'),
    # path('catalog/books/')
    # path('catalog/authors/')
    # path('catalog/book/<id>/')
    # path('catalog/author/<id>/')
    # path('catalog/books/')
]
