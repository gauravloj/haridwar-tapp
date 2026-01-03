from django.urls import path
from . import views

app_name = 'services'

urlpatterns = [
    path('', views.home, name='home'),
    path('services/', views.service_list, name='service_list'),
    path('services/<int:pk>/', views.service_detail, name='service_detail'),
    path('services/<int:service_id>/book/', views.booking, name='booking'),
    path('payment/<int:booking_id>/', views.payment, name='payment'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/success/<int:booking_id>/', views.payment_success, name='payment_success'),
    path('payment/failed/<int:booking_id>/', views.payment_failed, name='payment_failed'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
]
