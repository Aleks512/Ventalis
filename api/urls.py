from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
#from .admin_views import get_all_consultants
from .admin_views import AllConsultantsView, ConsultantCreateView, ConsultantDetailView, ConsultantDeleteView

urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #path('api-consultants/', get_all_consultants, name='get_all_consultants'),
    path('api-consultants/', AllConsultantsView.as_view(), name='show-consultants'),
    path('api-create-consultant/', ConsultantCreateView.as_view(), name='create-consultant'),
    path('api-retreive-consultant/<int:pk>', ConsultantDetailView.as_view(), name='retreive-consultant'),
    #path('api-update-consultant/<int:pk>', ConsultantUpdateView.as_view(), name='update-consultant'),
    path('api-delete-consultant/<int:pk>', ConsultantDeleteView.as_view(), name='delete-consultant'),

]