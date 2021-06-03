
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    path('task/<str:pk>/', views.taskDetail, name='task'),
    path('create', views.createTask, name='create'),
    path('update/<str:pk>/', views.updateTask, name='update'),
    path('delete/<str:pk>/', views.deleteTask, name='delete'),
    
    path('login/', views.loginUser, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('register/', views.registerUser, name='register'),
    
]