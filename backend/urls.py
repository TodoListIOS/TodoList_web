"""TodoList_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path, include

from backend import views

urlpatterns = [
    path('', views.web_login, name='web_login'),
    path('logout/', views.web_logout, name='web_logout'),
    path('web_register', views.web_register, name='web_register'),
    path('login_api/', views.login_api, name='login_api'),
    path('register_api/', views.register_api, name='register_api'),
    path('password_find_back_api/', views.password_find_back_api, name='password_find_back_api'),
    path('json_transfer/', views.json_transfer, name='json_transfer'),
    path('homepage/', views.homepage, name='homepage'),
    path('web_feed_back/', views.web_feed_back, name='web_feed_back'),
    path('web_password_find_back/', views.web_password_find_back, name='web_password_find_back'),
]
