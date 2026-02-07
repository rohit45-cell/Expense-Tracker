from django.shortcuts import render, redirect
from django.views import View
import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from validate_email import validate_email
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


# ==============================
# USERNAME VALIDATION (AJAX)
# ==============================
class UsernameValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        username = data.get('username', '').strip()

        if not username:
            return JsonResponse({'username_error': 'Username is required'}, status=400)

        if not username.isalnum():
            return JsonResponse(
                {"username_error": "Username should contain only letters and numbers"},
                status=400
            )

        if User.objects.filter(username=username).exists():
            return JsonResponse(
                {'username_error': 'Username already exists'},
                status=409
            )

        return JsonResponse({"username_valid": True}, status=200)


# ==============================
# EMAIL VALIDATION (AJAX)
# ==============================
class EmailValidationView(View):
    def post(self, request):
        try:
            data = json.loads(request.body.decode('utf-8'))
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

        email = data.get('email', '').strip()

        if not email:
            return JsonResponse({'email_error': 'Email is required'}, status=400)

        if not validate_email(email):
            return JsonResponse(
                {"email_error": "Email is invalid"},
                status=400
            )

        if User.objects.filter(email=email).exists():
            return JsonResponse(
                {'email_error': 'Email already exists'},
                status=409
            )

        return JsonResponse({"email_valid": True}, status=200)


# ==============================
# REGISTER
# ==============================
class RegisterationView(View):
    def get(self, request):
        return render(request, 'authentication/register.html')

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        context = {
            'fieldvalues': request.POST
        }

        if not username or not email or not password:
            messages.error(request, 'All fields are required')
            return render(request, 'authentication/register.html', context)

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken')
            return render(request, 'authentication/register.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already taken')
            return render(request, 'authentication/register.html', context)

        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return render(request, 'authentication/register.html', context)

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        messages.success(request, 'Account created successfully. Please login.')
        return redirect('login')


# ==============================
# LOGIN
# ==============================
class LoginView(View):
    def get(self, request):
        return render(request, 'authentication/login.html')

    def post(self, request):
        username = request.POST.get('username')
        password = request.POST.get('password')

        if not username or not password:
            messages.error(request, 'Please fill all fields')
            return render(request, 'authentication/login.html')

        user = authenticate(username=username, password=password)

        if user is None:
            messages.error(request, 'Invalid username or password')
            return render(request, 'authentication/login.html')

        login(request, user)
        messages.success(request, f'Welcome {user.username}')
        return redirect('home')


# ==============================
# LOGOUT
# ==============================
class LogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('login')


# ==============================
# PROFILE
# ==============================
class ProfileView(LoginRequiredMixin, View):
    login_url = 'login'

    def get(self, request):
        return render(
            request,
            'authentication/profile.html',
            {'user': request.user}
        )

    def post(self, request):
        user = request.user
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        password = request.POST.get('password')

        user.first_name = first_name
        user.last_name = last_name

        if password:
            if len(password) < 6:
                messages.error(request, "Password must be at least 6 characters")
                return redirect('profile')
            user.set_password(password)

        user.save()
        messages.success(request, "Profile updated successfully")
        return redirect('profile')


# ==============================
# DELETE PROFILE
# ==============================
@login_required(login_url='login')
def deleteProfile(request):
    user = request.user
    user.delete()
    messages.success(request, 'Account deleted successfully')
    return redirect('register')
