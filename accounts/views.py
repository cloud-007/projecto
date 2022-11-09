from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import User


class HomeView(View):
    template_name = 'base.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class SignInView(View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):

        print(request.POST)
        username = request.POST.get("email")
        password = request.POST.get("password")
        messages.success(request, '')
        user = authenticate(username=username, password=password)
        if user is not None:
            print("successful")
            login(request, user)
            messages.success(request, 'Welcome ' + user.username)
            return redirect('home')
        else:
            return render(request, self.template_name, {})


class SignOutView(View):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class RegisterView(View):
    template_name = 'accounts/register.html'

    context = {
        'username': '',
        'student_id': '',
        'email': '',
        'password': '',
        'confirm_password': '',
    }

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        student_id = request.POST.get("student_id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        # saving data so that they are not cleared when re-rendered
        self.context = {
            'username': username,
            'student_id': student_id,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
        }
        # checking if the user already exist of not
        if User.objects.filter(username=username).first():
            messages.error(request, "This username is already taken")
            return render(request, self.template_name, context=self.context)

        # checking if all the fields is ok or not
        if username and student_id and email and password and confirm_password and password == confirm_password:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            if user:
                print("Registration Successful")
                messages.success(request, 'Your account has been created! Login Please')
                return redirect('login')
        # create user account and redirect to login
        return render(request, self.template_name, context=self.context)
