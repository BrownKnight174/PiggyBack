from django.urls import path
from . import views

urlpatterns = [
    path('', views.ProductPage.as_view(), name='ProductPage'),
    path('payment/', views.PaymentsPage.as_view(), name='PaymentsPage'),
    path('paymentportal/', views.PaymentPortalPage.as_view(), name='PaymentsPage'),
]