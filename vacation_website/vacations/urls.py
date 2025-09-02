from django.urls import path
from . import views

urlpatterns = [
    path('', views.vacation_list_view, name='vacation_list'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('login-simple/', views.login_simple_view, name='login_simple'),
    path('logout/', views.logout_view, name='logout'),
    path('add/', views.add_vacation_view, name='add_vacation'),
    path('edit/<int:vacation_id>/', views.edit_vacation_view, name='edit_vacation'),
    path('delete/<int:vacation_id>/', views.delete_vacation_view, name='delete_vacation'),
    path('like/<int:vacation_id>/', views.toggle_like_view, name='toggle_like'),
]