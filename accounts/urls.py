from django.urls import path
from django.contrib.auth import views as auth_views

from . import views as user_views

urlpatterns = [
    path('login/', user_views.login, name='login'),
    path('register/', user_views.register, name='register'),
    path('logout/', user_views.logout, name='logout'),
    path('profile/', user_views.profile, name='profile'),

    path('password-reset/', auth_views.PasswordResetView.as_view(
        template_name='accounts/password_reset.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(
        template_name='accounts/password_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='accounts/password_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='accounts/password_reset_complete.html'), name='password_reset_complete'),
]
