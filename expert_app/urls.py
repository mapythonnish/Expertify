# urls.py
from django.urls import path
from . import views

urlpatterns = [
    
    path('master-admin-login/', views.MasterAdminLoginAPIView.as_view(), name='master-admin-login'),
    path('create-owner/', views.OwnerCreateAPIView.as_view(), name='create-owner'),
    path('owner/login/', views.OwnerLoginAPIView.as_view(), name='admin_login'),
    path('change-password/', views.PasswordChangeAPIView.as_view(), name='change-password'),
    path('reset-password/', views.SendPasswordResetEmailView.as_view(), name='reset-password'),
    path('reset-password/<uidb64>/<token>/', views.PasswordResetAPIView.as_view(), name='reset-password-confirm'),
    path('signup/', views.ExpertSignUpAPIView.as_view(), name='expert-signup'),
    path('profile/', views.ExpertProfileAPIView.as_view(), name='expert-profile'),
    path('expert/login/', views.ExpertLoginAPIView.as_view(), name='user_login'), 
    path('notifications/', views.OwnerNotificationAPIView.as_view(), name='owner-notifications'),# Endpoint for user login
    path('expert-change-password/', views.ExpertPasswordChangeAPIView.as_view(), name='change-password'),
    path('expert-send-password-reset-email/', views.ExpertSendPasswordResetEmailView.as_view(), name='send-password-reset-email'),
    path('expert-password-reset/<uidb64>/<token>/', views.ExpertPasswordResetAPIView.as_view(), name='password-reset'),
    path('notifications/<int:notification_id>/delete/', views.NotificationDeleteAPIView.as_view(), name='notification-delete'),

    #path('notifications/', views.NotificationListView.as_view(), name='notification-list'),
]

   

