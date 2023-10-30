from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    #path('communication/', include('communication.urls')),
    path('messagerie/', include('messagerie.urls')), # Assurez-vous que le nom correspond à votre application.
]
