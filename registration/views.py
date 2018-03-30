from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib import messages


class LandingPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'landing.html', context=None)

class HomePage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'home.html', context=None)

    def post(self, request, **kwargs):
        email = request.POST.get("email")
        password = request.POST.get("password")
        user = authenticate(username = email, password =  password)
        if user is not None:
            # Session cookies
            return render(request, 'home.html', context=None)
        else:
            messages.error(request, "Login unsuccessful!")
            return render(request, 'home.html', context=None)

class SignUpPage(TemplateView):
    def get(self, request, **kwargs):
        return render(request, 'signup.html', context=None)

    def post(self, request, **kwargs):
        email = request.POST.get("user[email]")
        pass1 = request.POST.get("user[password]")
        pass2 = request.POST.get("user[password2]")

        if User.objects.filter(username=email).exists():
            messages.error(request, "Email already registered!")
            return render(request, 'signup.html', context=None)

        if pass1 != pass2:
            messages.error(request, "Password mismatch!")
            return render(request, 'signup.html', context=None)

        else:
            # Add user to database
            user = User.objects.create_user(email, email, pass1)
            user.save()
            return redirect('HomePage')
