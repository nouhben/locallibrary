from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import login_required
@login_required
def all_users(request):
    # using the decorator  @login_required is same as using:
    #if request.user.is_authenticated ...
    pass
#using the restriction with class based views
# from django.contrib.auth.mixins import LoginRequiredMixin
# class MyView(LoginRequiredMixin, View):
#     #login_url = '/login/'
#     #redirect_field_name = 'redirect_to' # this has the same effext as 'next' in function based views
# This has exactly the same redirect behaviour as the login_required decorator. 
# You can also specify an alternative location to redirect the user to if they are not authenticated (login_url), 
# and a URL parameter name instead of "next" to insert the current absolute path (redirect_field_name). 
    
def register(request):
    return render(request, 'users/register.html',{'title':'Sign up'})