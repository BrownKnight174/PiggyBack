from django.urls import path
from . import views

urlpatterns = [
    path('', views.LandingPage.as_view(), name='LandingPage'),
    path('signup/', views.SignUpPage.as_view(), name='SignUpPage'),
    path('home/', views.HomePage.as_view(), name='HomePage'),
    path('logout/', views.logout_view, name='LogoutPage'),
    path('invite/', views.InvitePage.as_view(), name='InvitePage'),
]
