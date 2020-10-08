from django.shortcuts import render

# Create your views here.
from catalog.models import Book, BookInstance, Author, Genre, Language
def index(request):
    # Get a session value, setting a default if it is not present
    # num_visits = request.session.get('num_visits',0)
    # if request.session['num_visits']:
    #     request.session['num_visits'] = num_visits + 1
    # Number of visits to this view, as counted in the session variable.
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1
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
        'num_visits': num_visits,
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


class AuthorListView(ListView):
    model = Author
    context_object_name = 'authors'
    paginate_by = 10

    def get_queryset(self):
        return Author.objects.all()
    def get_context_data(self, **kwargs):
        # Call the base implementation first to get the context
        context = super(AuthorListView, self).get_context_data(**kwargs)
        # Create any data and add it to the context
        context['this_work'] = BookInstance.objects.all().count()
        return context

class AuthorDetailView(DetailView):
    model = Author