from django.conf import settings # new
from django.conf.urls.static import static

from django.contrib import admin
from django.contrib.auth.views import PasswordResetView, PasswordResetDoneView, PasswordResetConfirmView, \
    PasswordResetCompleteView
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView

from api import consultant_views, customer_views
from api.consultant_views import OrderItemUpdateView, ConsultantOrderItemsView
from api.customer_views import ViewCustomerConsultant
from api.message_views import CustomerApiMessageViewSet, ApiMessageCreateView, ConsultantApiMessageViewSet, \
    MessagesWrittenByCustomerApiMessageViewSet, ConsultatReadApiMessageViewSet, CustomerApiMessageCreateView

router = DefaultRouter()
# router.register(r'newusers', views.NewUserViewSet)
#router.register(r'customer-messages', CustomerApiMessageViewSet, basename='customer-message')

from Ventalis import settings

urlpatterns = ([
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('messagerie/', include('messagerie.urls')),
    path('', include('store.urls')),
    path('', include('api.urls')),
    path('', include('contact.urls')),
    # API patths

    path('consultant-orderitems/', ConsultantOrderItemsView.as_view(), name='consultant_orderitems'),
    path('consultant-orderitem-update/<int:pk>/', OrderItemUpdateView.as_view(), name='orderitem_update'),

    path('consultant-create-message/', ApiMessageCreateView.as_view(), name='consultant-create-message'),
    path('consultant-sent-messages/', ConsultantApiMessageViewSet.as_view({'get': 'list'}),name='consultant-sent-messages'),
    path('consultant-read-messages/', ConsultatReadApiMessageViewSet.as_view({'get': 'list'}), name='consultant-read-messages'),

    path('customer-create-message/', CustomerApiMessageCreateView.as_view(), name='customer-create-message'),
    path('customer-sent-messages/', MessagesWrittenByCustomerApiMessageViewSet.as_view({'get': 'list'}),name='customer-sent-messages'),
    path('customer-read-messages/', CustomerApiMessageViewSet.as_view({'get': 'list'}), name='customer-read-messages'),


    path('customer-consultant/', ViewCustomerConsultant.as_view(), name='view-customer-consultant'),

    path('customer-orderitems/', customer_views.OrderItemListAPIView.as_view(), name='order_item_list'),
    path('customer-orderitem/<int:id>/', customer_views.OrderDetailAPIView.as_view(), name='order_detail'),




    path('api-auth/', include('rest_framework.urls')),
    path("api/", include(router.urls)),
    path('api/schema/',SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/docs/',SpectacularSwaggerView.as_view(url_name='schema')),

    path('reset-password/',
       PasswordResetView.as_view(template_name="registration/password_reset.html"),
       name='reset_password'),
    path('reset-password/done/',
       PasswordResetDoneView.as_view(template_name='registration/password_reset_done1.html'),
       name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/',
       PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm1.html'),
       name='password_reset_confirm'),
    path('reset-password/complete/',
       PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete1.html'),
                       name='password_reset_complete'),

])

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT) # to render the photos uploaded if not 404
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)



