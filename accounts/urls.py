from django.urls import path
from .views import register, login_view, logout_view, activate
from django.contrib.auth.views import (
    PasswordResetView, 
    PasswordResetDoneView, 
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

urlpatterns = [
	path('register/', register, name='register'),
    path('activate/<uidb64>/<token>', activate, name='activate'),
	path('login/', login_view, name='login'),
	path('logout/', logout_view, name='logout'),
    path('password-reset/', PasswordResetView.as_view(
        template_name='accounts/password_reset.html'),
        name='password-reset'
    ),
]