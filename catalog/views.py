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

from django.contrib.auth.mixins import LoginRequiredMixin
class LoanedBooksByUserListView(LoginRequiredMixin, ListView):
    model = BookInstance
    template_name = 'catalog/bookinstance_list_borrowed_user.html'
    paginate_by= 5
    context_object_name = 'mybooks'
    def get_queryset(self):
        return BookInstance.objects.filter(borrower=self.request.user).filter(loan_status__exact='O').order_by('due_back_date')

from django.contrib.auth.mixins import PermissionRequiredMixin
class LoanedBookListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = BookInstance
    paginate_by= 10
    context_object_name = 'mybooks'
    template_name = 'catalog/bookinstance_list_borrowed_librarian.html'
    #permission_required = 'catalog.can_mark_returned'
    # Or multiple permissions
    permission_required = ('catalog.can_mark_returned')
    def get_queryset(self):
        return BookInstance.objects.filter(loan_status__exact='O').order_by('due_back_date')

from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.http import HttpResponseRedirect
@permission_required('catalog.can_mark_returned')
def mark_book_returned(request, instance_id):
    instance = get_object_or_404(BookInstance, id=instance_id)
    instance.loan_status = 'M'
    instance.borrower = None
    instance.due_back_date = None
    instance.save()

    return HttpResponseRedirect(reverse('borrowed-books'))

from .forms import RenewBookForm
import datetime

@permission_required('catalog.can_mark_returned')
def renew_book_librarian(request, instance_id):
    """View function for renewing a specific BookInstance by librarian."""
    instance = get_object_or_404(BookInstance, id=instance_id)
    # If this is a POST request then process the Form data
    if request.method == 'POST':
        # Create a form instance and populate it with data from the request (binding):
        form = RenewBookForm(request.POST)
        # Check if the form is valid:
        if form.is_valid():
             # process the data in form.cleaned_data as required (here we just write it to the model due_back field)
             instance.due_back_date = form.cleaned_data['renewal_date']
             instance.save()
             return HttpResponseRedirect(reverse('borrowed-books'))
    # If this is a GET (or any other method) create the default form.
    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBookForm(initial={'renewal_date':proposed_renewal_date})

    context = {
        'form':form,
        'book_instance':instance,
    }
    return render(request,'catalog/book_renew_librarian.html',context)

from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from catalog.models import Author, Book, BookInstance


class AuthorCreate(PermissionRequiredMixin, CreateView):
    #multiple permissions
    permission_required = ('catalog.can_create_author',)
    model = Author
    fields = '__all__'
    initial = {'date_of_death': '05/01/2018'}

class AuthorUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('catalog.can_create_author',)
    model = Author
    fields = ['name','date_of_birth', 'date_of_death']

class AuthorDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('catalog.can_create_author',)
    model = Author
    success_url = reverse_lazy('authors')

#Books
class BookCreate(PermissionRequiredMixin, CreateView):
    permission_required = ('catalog.can_create_author',)
    model = Book
    fields = '__all__'
    #initial = {'date_of_death': '05/01/2018'}

class BookUpdate(PermissionRequiredMixin, UpdateView):
    permission_required = ('catalog.can_create_author',)
    model = Book
    fields = ['name','date_of_birth', 'date_of_death']

class BookDelete(PermissionRequiredMixin, DeleteView):
    permission_required = ('catalog.can_create_author',)
    model = Book
    success_url = reverse_lazy('authors')