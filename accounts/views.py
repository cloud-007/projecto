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
        'full_name': '',
        'batch': '',
        'section': '',
    }

    def get(self, request, *args, **kwargs):
        logout(request)
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("student_id")
        student_id = request.POST.get("student_id")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        full_name = request.POST.get("full_name")
        batch = request.POST.get("batch")
        section = request.POST.get("section")
        # saving data so that they are not cleared when re-rendered
        self.context = {
            'username': username,
            'student_id': student_id,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'full_name': full_name,
            'batch': batch,
            'section': section,
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
            student_profile = Student.objects.create(full_name=full_name, student_id=student_id, batch=batch,
                                                     section=section,
                                                     user_id=user.id)
            if student_profile:
                student_profile.save()
                # create user account and redirect to log in
                print("Registration Successful")
                messages.success(request, 'Your account has been created! Login Please')
                return redirect('login')
            else:
                user.delete()
        else:
            messages.warning(request, "Password and Confirm password isn't same!")
            return render(request, self.template_name, context=self.context)

        return render(request, self.template_name, context=self.context)


class ProfileView(View):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        student_profile = Student.objects.filter(user_id=request.user).first()
        if student_profile:
            print("Student object Found")
            context = {
                'student': student_profile
            }
            return render(request, self.template_name, context=context)
        else:
            context = {
                'student': Student()
            }
            print("Student object not Found")

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        print(request.POST.get("profile_image"))
        full_name = request.POST.get("full_name")
        student_id = request.POST.get("student_id")
        batch = request.POST.get("batch")
        section = request.POST.get("section")

        has_profile_image = False
        if len(request.POST.get("profile_image", "")) > 0:
            has_profile_image = True

        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, '')

        check_student_id = Student.objects.filter(student_id=student_id).first()
        if check_student_id and request.user.student.student_id != check_student_id.student_id:
            messages.warning(request, 'This student id already exists')
            context = {
                'student': ''
            }
            if request.user.student:
                context = {
                    'student': request.user.student
                }
            return render(request, self.template_name, context=context)

        previous_student_profile = Student.objects.filter(user_id=request.user).first()

        if previous_student_profile and previous_student_profile.user == request.user:
            previous_student_profile.student_id = student_id
            previous_student_profile.full_name = full_name
            previous_student_profile.batch = batch
            previous_student_profile.section = section
            if has_profile_image:
                previous_student_profile.profile_image = request.FILES['profile_image']
            previous_student_profile.user = request.user
            messages.success(request, "Your profile has been updated.")
            previous_student_profile.save()
            print("Successful")
            context = {
                'student': previous_student_profile
            }
        else:
            if has_profile_image:
                student = Student(
                    full_name=full_name,
                    student_id=student_id,
                    batch=batch,
                    section=section,
                    profile_image=request.FILES['profile_image'],
                    user=request.user
                )
            else:
                student = Student(
                    full_name=full_name,
                    student_id=student_id,
                    batch=batch,
                    section=section,
                    user=request.user
                )
            student.save()
            context = {
                'student': student
            }

        return render(request, self.template_name, context=context)
