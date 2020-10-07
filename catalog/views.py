from django.shortcuts import render

# Create your views here.
from catalog.models import Book, BookInstance, Author, Genre, Language
def index(request):
    books = Book.objects.all()
    instances = BookInstance.objects.all()
    authors = Author.objects.all()

    num_available_instances = instances.filter(loan_status__exact='A').count()

    context = {
        'num_books':books.count(),
        'num_instances': instances.count(),
        'num_authors': authors.count(),
        'num_available_instances': num_available_instances,
        'title':'Home',
    }
    return render(request,'catalog/index.html', context=context)
