from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
urlpatterns = [
    path('admin/', admin.site.urls),
    path('catalog/', include('catalog.urls')),
    path('', RedirectView.as_view(url='catalog/', permanent=True)),
    path('accounts/', include('django.contrib.auth.urls')),
    path('users/', include('users.urls')),
    #Auth urls
    # path("accounts/login/[name='login']",include('django.contrib.auth.urls')),
    # path("accounts/logout/[name='logout']",include('django.contrib.auth.urls')),
    # path("accounts/password_change/[name='password_change']",include('django.contrib.auth.urls')),
    # path("accounts/password_change/done/[name='password_change_done']",include('django.contrib.auth.urls')),
    # path("accounts/password_reset/[name='password_reset']",include('django.contrib.auth.urls')),
    # path("accounts/password_reset/done/[name='password_reset_done']",include('django.contrib.auth.urls')),
    # path("accounts/reset/<uidb64>/<token>/[name='password_reset_confirm']",include('django.contrib.auth.urls')),
    # path("accounts/reset/done/[name='password_reset_complete']",include('django.contrib.auth.urls')),
]
