from django.urls import path
from . import views

urlpatterns = [

    path('', views.home, name='home'),

    # Customer
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('customer-logout/', views.customer_logout, name='customer_logout'),

    # Admin
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('admin-customers/', views.admin_customers, name='admin_customers'),
    path(
        'toggle-customer/<int:customer_id>/',
        views.toggle_customer_status,
        name='toggle_customer_status'
    ),
    path('admin-logout/', views.admin_logout, name='admin_logout'),

]