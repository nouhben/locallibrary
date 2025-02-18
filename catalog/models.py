from django.db import models
from django.urls import reverse
import uuid
# Create your models here.
class Author(models.Model):
    name = models.CharField(max_length=255)
    date_of_birth = models.DateField(auto_now=False,auto_now_add=False,null=True, blank=True)
    date_of_death = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name='Died')
    bio = models.TextField(max_length=1000, help_text='Enter a brief bio of the author', default='', blank=True, null=True)
    class Meta:
        ordering = ['name']
    def get_absolute_url(self):
        """Returns the url to access a particular author instance."""
        return reverse('author-detail', args=[str(self.id)])

    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=100,help_text='Enter a book genre (e.g. Science Fiction)')
    def __str__(self):
        return self.name
class Language(models.Model):
    name = models.CharField(max_length=100)
    def __str__(self):
        return self.name


class Book(models.Model):
    title = models.CharField(max_length=255)
    #Because some authors my not be declared yet
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True)
    summary = models.TextField(max_length=1000, help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN',max_length=13)
    genre = models.ManyToManyField(Genre, help_text='Select a genre for this book')
    language = models.ForeignKey(Language, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])

    def display_genre(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([genre.name for genre in self.genre.all()[:3]])
    display_genre.short_description = 'Genrex' #This is used like verbose_name for the function display_genre
    #when it is called from a view 'display_genre' just as we call a normal field

    def display_language(self):
        """Creates a string for the Genre. This is required to display genre in Admin."""
        return ', '.join([language.name for language in self.language.all()[:3]])
    display_language.short_description = 'Language'

from django.contrib.auth.models import User
from datetime import date
class BookInstance(models.Model):
    LOAN_STATUS = [
        ('M', 'Maintenance'),
        ('O', 'On loan'),
        ('A', 'Available'),
        ('R', 'Reserved'),
    ]
    id = models.UUIDField(primary_key=True, default=uuid.uuid4,help_text='Unique ID for this particular book across whole library')
    due_back_date = models.DateField(auto_now=False, auto_now_add=False, null=True, blank=True, verbose_name='Due Back')
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True)
    loan_status = models.CharField(max_length=1, choices=LOAN_STATUS, blank=True, default='m', help_text='Book availability',)
    imprint = models.CharField(max_length=255)
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    @property #it is like a setter
    def is_overdue(self):
        #the first elf.due_back_date is to make sure it is not null
        if self.due_back_date and date.today() > self.due_back_date:
            return True
        return False
    class Meta:
        ordering = ['-due_back_date']
        permissions = (('can_mark_returned','Set the book as returned'),)

    def __str__(self):
        return f'{self.id} {self.book.title}'

    def set_returned(self, **kwargs):
        self.loan_status = 'M'
        self.due_back_date = None
        self.borrower = None


