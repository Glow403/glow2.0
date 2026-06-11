from django.urls import path
from . import views
from .views import create_first_admin

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),
    path('create-admin/', create_first_admin, name='create_admin'),
    path('login/', views.user_login, name='login'),
    path('register/', views.user_register, name='register'),
    path('logout/', views.user_logout_view, name='logout'),
    path('services/', views.services, name='services'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('service/<str:service_type>/', views.service_page, name='service_page'),
]
