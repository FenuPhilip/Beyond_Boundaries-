from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('project-request/', views.project_request, name='project_request'),
    path('mentor-request/', views.mentor_request, name='mentor_request'),
    path('builder-join/', views.builder_join, name='builder_join'),
    path('success/', views.success, name='success'),

    # User account
    path('account/register/', views.user_register, name='user_register'),
    path('account/login/', views.user_login, name='user_login'),
    path('account/logout/', views.user_logout, name='user_logout'),
    path('account/', views.account_dashboard, name='account_dashboard'),
    path('account/settings/', views.account_settings, name='account_settings'),
    path('account/toggle-work-status/', views.toggle_work_status, name='toggle_work_status'),
]
