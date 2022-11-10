from django.urls import path
from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from users import views as user_views


urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard', views.index, name='index'),
    path('about/', user_views.home, name='about'),
    path('staff/', views.staff, name='dashboard-staff'),
    path('staff/detail/<int:pk>/', views.staff_detail, name='dashboard-staff'),
    path('index/', views.index, name='index'),
    path('product1/', views.product1, name='dashboard-product'),
    path('product/delete/<int:pk>/', views.product_delete, name='dashboard-product-delete'),
    path('product/update/<int:pk>/', views.product_update, name='dashboard-product-update'),
    path('order/', views.order, name='dashboard-order'),
    path('about/', views.home, name='about'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'),name='logout'),
    path('profile/', user_views.profile, name='user-profile'),
    path('profile/confirm-delivery/<int:pk>/', user_views.confirm_order, name="confirm-order"),
    path('profile/update/', user_views.profile_update, name='user-profile-update'),
    path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'),name='user-logout'),
    #path('product1/', user_views.product1, name='user-product'),
    path('staff/', user_views.staff, name='user-staff'),
    path('order/', user_views.order, name='user-order'),
    path('', auth_views.LoginView.as_view(template_name='user/login.html'), name='user-login'),
    path('register/', user_views.register, name='user-register'),
                

    

]
