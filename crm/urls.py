from django.urls import path
from . import views

from django.contrib.auth import views as auth_views

urlpatterns = [
    #-------------------- USER AUTHENTICATION --------------------#

    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutPage, name='logout'),

    #-------------------- FORGOT PASSWORD --------------------#

    path('reset_password/',
        auth_views.PasswordResetView.as_view(template_name='crm/authentication/password_reset.html'),
        name='reset_password'),
    path('reset_password_sent/',
        auth_views.PasswordResetDoneView.as_view(template_name='crm/authentication/password_reset_sent.html'),
        name='password_reset_done'),
    path('reset/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(template_name='crm/authentication/password_reset_form.html'),
        name='password_reset_confirm'),
    path('reset_password_complete/',
        auth_views.PasswordResetCompleteView.as_view(template_name='crm/authentication/password_reset_done.html'),
        name='password_reset_complete'),

    #-------------------- ADMIN URLS --------------------#

    path('', views.dashboard, name='dashboard'),
    path('products/', views.products, name='products'),
    path('viewCustomer/<str:id>/', views.viewCustomer, name='viewCustomer'),
    path('updateCustomer/<str:id>/', views.updateCustomer, name='updateCustomer'),

    #-------------------- CRUD OPERATIONS --------------------#
    
    path('createOrder/<str:id>', views.createOrder, name='createOrder'),
    path('createDashboardOrder/', views.createDashboardOrder, name='createDashboardOrder'),
    path('updateOrder/<str:id>/', views.updateOrder, name='updateOrder'),
    path('removeOrder/<str:id>/', views.removeOrder, name='removeOrder'),

    #-------------------- USER URLS --------------------#
    
    path('profile/', views.profile, name='profile'),
    path('customerDashboard', views.customerDashboard, name='customerDashboard'),
]