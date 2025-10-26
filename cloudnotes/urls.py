from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def redirect_to_notes(request):
    return redirect('/notes/')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('accounts.urls')),
    path('notes/', include('notes.urls')),
    path('', redirect_to_notes),  # Redirect root URL to /notes/
]
