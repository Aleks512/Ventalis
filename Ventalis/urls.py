from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from api.consultant_views import OrderItemUpdateView, ConsultantOrderItemsView
from api.message_views import CustomerApiMessageViewSet, ApiMessageCreateView

router = DefaultRouter()
# router.register(r'newusers', views.NewUserViewSet)
router.register(r'customer-messages', CustomerApiMessageViewSet, basename='customer-message')

from Ventalis import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('messagerie/', include('messagerie.urls')),
    path('', include('store.urls')),
    path('', include('api.urls')),
    # API patths
    path('consultant-create-message/', ApiMessageCreateView.as_view(), name='consultant-create-message'),
    path('orderitem-update/<int:pk>/', OrderItemUpdateView.as_view(), name='orderitem_update'),
    path('consultant-orderitems/', ConsultantOrderItemsView.as_view(), name='consultant_orderitems'),



    path('api-auth/', include('rest_framework.urls')),
    path("api/", include(router.urls)),
    path('api/schema/',SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/',SpectacularSwaggerView.as_view(url_name='schema')),


] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # to render the photos uploaded if not 404
