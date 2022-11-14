from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import User, Student


class SignInView(View):
    template_name = 'accounts/newlogin.html'

    def get(self, request, *args, **kwargs):

        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, '')
        user = authenticate(username=username, password=password)
        if user is not None:
            print("successful")
            login(request, user)
            return redirect('home')
        else:
            messages.warning(request, 'Your username or password is wrong! Please provide a valid credentials')
            return render(request, self.template_name, {})


class SignOutView(View):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('home')

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


class RegisterView(View):
    template_name = 'accounts/newRegister.html'

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
            messages.warning(request, "This username is already taken")
            return render(request, self.template_name, context=self.context)

        # checking if all the fields is ok or not
        if password == confirm_password:
            user = User.objects.create_user(username=username,
                                            email=email,
                                            password=password)
            if user:
                # create user account and redirect to log in
                print("Registration Successful")
                messages.success(request, 'Your account has been created! Login Please')
                return redirect('login')
        else:
            messages.warning(request, "Password and Confirm password isn't same!")
            return render(request, self.template_name, context=self.context)

        return render(request, self.template_name, context=self.context)


class ProfileView(View):
    template_name = 'accounts/profile.html'

    context = {
        'full_name': '',
        'student_id': '',
        'batch': '',
        'section': '',
        'image_url': '',
    }

    def get(self, request, *args, **kwargs):
        if Student.objects.filter(user=request.user).first():
            print("Student object Found")
            self.context = {
                'full_name': request.user.student.full_name,
                'student_id': request.user.student.student_id,
                'batch': request.user.student.batch,
                'section': request.user.student.section,
                'image_url': '',
            }
            return render(request, self.template_name, context=self.context)
        else:
            print("Student object not Found")

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        full_name = request.POST.get("full_name")
        student_id = request.POST.get("student_id")
        batch = request.POST.get("batch")
        section = request.POST.get("section")
        context = {
            'full_name': full_name,
            'student_id': student_id,
            'batch': batch,
            'section': section,
            'image_url': '',
        }

        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, '')

        student = Student.objects.filter(user=request.user).first()
        if student:
            student.student_id = student_id
            student.full_name = full_name
            student.batch = batch
            student.section = section
            messages.success(request, "Your profile has been updated.")
            student.save()
            print("Successful")
            return render(request, self.template_name, context)
        else:
            student = Student(full_name=full_name, student_id=student_id, batch=batch, section=section,
                              user=request.user)
            student.save()

        return render(request, self.template_name, context)
