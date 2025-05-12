from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

app_name = 'accounts'

urlpatterns = [
    # Authentication URLS
    path('login/', views.loginView, name='login'),
    path('register/', views.registerView, name='register' ),
    path('logout/', views.logoutView, name='logout'),

    # GMAIL RESET URLS
    path(
        'password-reset/',
        auth_views.PasswordResetView.as_view(
            email_template_name='registration/password_reset_email.html',
            success_url=reverse_lazy('accounts:password_reset_done')
        ),
        name='password_reset'
    ),
    path(
        'password-reset/done/',
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset_done'
    ),
    path(
        'reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            success_url=reverse_lazy('accounts:password_reset_complete')
        ),
        name='password_reset_confirm'
    ),
    path(
        'reset/done/',
        auth_views.PasswordResetCompleteView.as_view(),
        name='password_reset_complete'
    ),
]