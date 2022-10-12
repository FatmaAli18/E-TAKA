from django.urls import path

from . import views
from django.contrib.auth import views as auth_views

from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.index, name='index'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/detail/<int:pk>/', views.staff_detail, name='dashboard-staff'),
    path('index/', views.index, name='index'),
    path('product1/', views.product1, name='dashboard-product'),
    path('product/delete/<int:pk>/', views.product_delete, name='dashboard-product-delete'),
    path('product/update/<int:pk>/', views.product_delete, name='dashboard-product-update'),
    path('order/', views.order, name='dashboard-order'),
    path('home/', views.home, name='home'),
    path('about/', views.home, name='about'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(
        template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),
         name='logout'),
]
