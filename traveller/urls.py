from django.urls import path
from . import views

urlpatterns = [
    path('', views.TravellerPage.as_view(), name='TravellerPage'),
    path('verification/', views.VerificationPage.as_view(), name='VerificationPage'),
]