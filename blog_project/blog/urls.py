from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('blog/<slug:slug>/', views.blog_detail, name='blog_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile_view, name='profile'),
    path('create/', views.create_blog, name='create_blog'),
    path('edit/<slug:slug>/', views.edit_blog, name='edit_blog'),
    path('delete/<slug:slug>/', views.delete_blog, name='delete_blog'),
]
