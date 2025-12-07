from django.urls import path
from . import views

urlpatterns = [
    path('', views.article_list, name='index'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('create/', views.article_create, name='article_create'),
    path('article/edit/<int:pk>/', views.article_edit, name='edit_article'),
    path('article/delete/<int:pk>/', views.article_delete, name='delete_article'),
]