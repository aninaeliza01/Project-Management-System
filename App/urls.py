from django.urls import path
from . import views


urlpatterns = [
    path('', views.custom_login, name='login'),
    path('login', views.custom_login, name='login'),  
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('register/', views.register, name='register'),
    path('logout/', views.logout_user,name="logout"),
    path('add_client/', views.add_client, name='add_client'),
    path('update_client/<int:client_id>/', views.update_client, name='update_client'),
    path('delete_client/<int:client_id>/', views.delete_client, name='delete_client'),
    path('project', views.project, name='project'),
    path('update_project/<int:pk>/', views.update_project, name='update_project'),
    path('delete_project/<int:pk>/', views.delete_project, name='delete_project'),
]
