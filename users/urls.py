from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView,PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView

urlpatterns=[
    path('', views.home, name="home"),
    path('presentation/', views.presentation, name="presentation"),
    path('login/', views.WebAppLoginView.as_view(template_name='registration/login.html'), name='login'),
    #path('login/', LoginView.as_view(template_name='registration/login.html',redirect_authenticated_user=True), name = 'login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path("consultant/add/", views.ConsultantCreateView.as_view(), name="consultant-add"),
    path('consultant/update/<pk>', views.ConsultantUpdate.as_view(), name="consultant-update"),
    path('consultant/delete/<pk>/', views.ConsultantDelete.as_view(), name="consultant-delete"),
    path("consultants/list/", views.ConsultantListView.as_view(), name="consultant-list"),
    path("customer/inscription/",  views.SignUp.as_view(), name="signup"),
    path('customers/list/', views.CustomerListView.as_view(), name='customers-list'),
    #path('consultant/',views.home_consultant, name="consultant-home"),
    #path('consultant/<str:matricule>/', views.consultant_profile, name='consultant_profile'),
    path('consultant/<str:matricule>/',views.ConsultantHome.as_view(), name="consultant-home"),
    path('customer/<int:id>/',views.CustomerHome.as_view(), name="customer-home"),
    #path('consultant/<str:pk>/', views.ConsultantHome.as_view(), name="consultant-home"),

    path('reset-password/',
         PasswordResetView.as_view(template_name="registration/password_reset.html"),
         name='reset_password'),
    path('reset-password/done/', PasswordResetDoneView.as_view(template_name='registration/password_reset_done1.html'),name='password_reset_done'),
    path('reset-password/confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='registration/password_reset_confirm1.html'),name='password_reset_confirm'),
    path('reset-password/complete/', PasswordResetCompleteView.as_view(template_name='registration/password_reset_complete1.html'),name='password_reset_complete'),

]
