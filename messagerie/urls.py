from django.urls import path

from . import views
from .views import ListThreads, \
                    CreateThread, \
                    ThreadView, \
                    CreateMessage

urlpatterns = [
    path('inbox/', ListThreads.as_view(), name='inbox'),

    path('inbox/create-thread/', CreateThread.as_view(), name='create-thread'),

    path('inbox/<int:pk>/', ThreadView.as_view(), name='thread'),

    path('inbox/<int:pk>/create-message/', CreateMessage.as_view(), name='create-message')
]