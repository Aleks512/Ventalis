from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Ventalis import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    #path('communication/', include('communication.urls')),
    path('messagerie/', include('messagerie.urls')),
    path('', include('store.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', include('api.urls')),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # to render the photos uploaded if not 404
