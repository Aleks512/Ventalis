from django.urls import path
from . import views
from django.contrib.auth.views import LoginView, LogoutView,PasswordResetView, PasswordResetDoneView, PasswordResetCompleteView, PasswordResetConfirmView

from .views import ConsultantListView, CustomerListView, NewUserListView

urlpatterns=[
    path('', views.home, name="home"),
    path('signup/', views.signup, name='signup'),
    path('consultant-signup/', views.consultant_signup, name='consultant-signup'),
    path("consultants/", ConsultantListView.as_view()),
    path("customers/", CustomerListView.as_view()),
    path("all-users/", NewUserListView.as_view()),
    path('login/', views.WebAppLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
]
