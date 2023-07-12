from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('profile/<int:pk>/', views.user_profile, name='profile'),
    path('account/', views.user_account, name='account'),
    path('register/', views.register_user, name='register'),
    path('activate/<uidb64>/<token>/', views.activate, name ='activate'),
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('update-user-profile/', views.update_user_profile, name='update-user-profile'),
    path('delete-user-profile/', views.delete_user_profile, name='delete-user-profile'),
    path('change-password/', views.change_password, name ='change-password'),
    path('reset_password/', views.password_reset_custom, name ='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='password_reset_done.html'), name ='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='password_reset_confirm.html'), name ='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='password_reset_complete.html'), name ='password_reset_complete'),

]