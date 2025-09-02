from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('stats/vacations/', views.vacation_stats, name='vacation_stats'),
    path('total/users/', views.total_users, name='total_users'),
    path('total/likes/', views.total_likes, name='total_likes'),
    path('distribution/likes/', views.likes_distribution, name='likes_distribution'),
]