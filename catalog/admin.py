from django.contrib import admin

# Register your models here.
from catalog.models import Genre, Language, Author, Book, BookInstance
admin.site.register(Genre)
#admin.site.register(Author)
#admin.site.register(Book)
admin.site.register(Language)
#admin.site.register(BookInstance)

class BookInline(admin.TabularInline):
    model = Book
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name','date_of_birth','date_of_death')
    #using ('date_of_birth', 'date_of_death') will display these fields horizontally
    fields = ['name', ('date_of_birth', 'date_of_death')]
    inlines = [BookInline]
    
#register the model with its corresponding new admin view instead of the default view
admin.site.register(Author, AuthorAdmin)

#This class is to get info about instances inside the detail view of the model book
class BooksInstanceInline(admin.TabularInline):
    model = BookInstance
#Register the Admin classes for BookInstance using the decorator
#the @register decorator to register the models 

#(this does exactly the same thing as the admin.site.register(BookInstance)
@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title','author','display_genre')
    inlines = [BooksInstanceInline]


@admin.register(BookInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('book','loan_status','due_back_date',)
    list_filter = ('book','loan_status','due_back_date')
    #To section the detail view of bookInstance into groups: the info related to someting put theme in a 
    #section together
    fieldsets = (
        ('Instance Info',{
            'fields':('book','imprint','id'),
        }),
        ('Availability',{
            'fields':('loan_status','due_back_date')
        }),
    )

