from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('gallery/', views.gallery, name='gallery'),
    path('item/<int:pk>/', views.item_detail, name='item_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Admin URLs
    path('admin/login/', views.admin_login, name='admin_login'),
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin/add/', views.add_item, name='add_item'),
    path('admin/edit/<int:pk>/', views.edit_item, name='edit_item'),
    path('admin/delete/<int:pk>/', views.delete_item, name='delete_item'),
    path('admin/logout/', views.admin_logout, name='admin_logout'),
]
