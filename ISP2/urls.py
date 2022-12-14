"""ISP2 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from users import views as user_views
from mpesa.urls import mpesa_urls
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
                  path('admin/', admin.site.urls),

                  path('about/', user_views.home, name='about'),
                  path('', include('users.urls')),
                  path('product1/', user_views.product1, name='user-product'),
                  path('staff/', user_views.staff, name='user-staff'),


                  path('order/', user_views.order, name='user-order'),
                  path('', auth_views.LoginView.as_view(
                      template_name='user/login.html'), name='user-login'),
                  path('register/', user_views.register, name='user-register'),
                  path('profile/', user_views.profile, name='user-profile'),
                  path('profile/update/', user_views.profile_update, name='user-profile-update'),
                  path('logout/', auth_views.LogoutView.as_view(template_name='user/logout.html'),
                       name='user-logout'),
                  
                path('mpesa/', include(mpesa_urls)),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
