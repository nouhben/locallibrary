from django.shortcuts import render

# Create your views here.
from catalog.models import Book, BookInstance, Author, Genre, Language
def index(request):
    books = Book.objects.all()
    instances = BookInstance.objects.all()
    authors = Author.objects.all()
    books_containing_x = books.filter(title__icontains='mark') | books.filter(summary__icontains='mark')

    num_available_instances = instances.filter(loan_status__exact='A').count()

    context = {
        'num_books':books.count(),
        'num_instances': instances.count(),
        'num_authors': authors.count(),
        'num_available_instances': num_available_instances,
        'books_containing_x':books_containing_x.count(),
        'genre_containing_x':Genre.objects.filter(name__icontains='fanta').count(),
        'title':'Home',
    }
    return render(request,'catalog/index.html', context=context)

from django.views.generic import DetailView, ListView

class BookListView(ListView):
    model = Book
    context_object_name = 'books' #default is: book_list
    queryset = Book.objects.filter(title__icontains='E-C')[:5] #five books that the title contains the word 'ma'
    #template_name = 'books/my_arbitrary_template_name_list.html'
    paginate_by = 3

    def get_queryset(self):
        return Book.objects.filter(title__icontains='E-C')[:5]
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(BookListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['num_of_instances'] = BookInstance.objects.all().count()
        return context

class BookDetailView(DetailView):
    model = Book

# def book_detail_view(request, primary_key):
#     try:
#         book = Book.objects.get(pk=primary_key)
#     except Book.DoesNotExist:
#         raise Http404('Book does not exist')
    
#     return render(request, 'catalog/book_detail.html', context={'book': book})
# from django.shortcuts import get_object_or_404

# def book_detail_view(request, primary_key):
#     book = get_object_or_404(Book, pk=primary_key)
#     return render(request, 'catalog/book_detail.html', context={'book': book})

