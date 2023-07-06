from django.urls import path
from . import views
from django.contrib.auth.views import (
    PasswordResetView,
    PasswordResetDoneView,
    PasswordResetConfirmView,
)
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('login/',views.user_login,name='login'),
    path('signup/',views.user_signup,name='signup'),
    path('logout/',views.user_logout,name='logout'),
    path('password-reset/',PasswordResetView.as_view(template_name='accounts/password_reset.html',html_email_template_name='accounts/password_reset_email.html'),name="password-reset"),
    path('password-reset/done/',PasswordResetDoneView.as_view(template_name='accounts/reset_password_done.html'),name="password_reset_done"),
    path('password-reset-confirm/<uidb64>/<token>/',PasswordResetConfirmView.as_view(template_name="accounts/password_reset_confirm.html"),name="password_reset_confirm"),
    # path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name="accounts/login.html"),name="password_reset_complete"),
    path('password-reset-complete/',views.PasswordResetComplete,name="password_reset_complete"),
    path('change-password/', auth_views.PasswordChangeView.as_view(template_name= 'accounts/change-password.html',success_url="/home/"),name="change_password"),

]