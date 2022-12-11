import json
import os

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views import View

from accounts.models import User, Student, Teacher, Token
from project_management.mixins import SuperUserMixin
from projecto.task import send_registration_email


class SignInView(View):
    template_name = 'accounts/login.html'

    def get(self, request, *args, **kwargs):
        resend_email = request.GET.get('resend_email', None)
        username = request.GET.get('username', None)

        if resend_email:

            user = User.objects.filter(username=username).first()
            user_id = urlsafe_base64_encode(force_bytes(user.pk))

            pre_token = Token.objects.filter(user=user)
            pre_token.delete()

            token = default_token_generator.make_token(user=user)
            token_table_data = Token(user=user, token=token)
            token_table_data.save()
            subject = 'Email Verification of PROJECTO'
            prefix = request.build_absolute_uri('account-confirmation/' + user_id + '/' + token)
            print(prefix)
            prefix = prefix.replace("login", "register")
            print(prefix)
            message = f"Hello {user.student.full_name}\n\nPlease go to the following link to verify your account.\n\n" \
                      f"{prefix}\n\n" \
                      f"Sincerely," \
                      f"\nYour Projecto Team! "
            from_email = os.environ.get('EMAIL_HOST_USER')
            if subject and message and from_email:
                send_registration_email.delay(user_id=user_id, subject=subject, message=message,
                                              email=user.email)
                messages.success(request,
                                 'An email will be send shortly. Follow the link to '
                                 'verify your account.')
                print("Email has been sent")
                return redirect('login')
            else:
                token_table_data.delete()
                return HttpResponse('Make sure all fields are entered and valid.')
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        password = request.POST.get("password")
        storage = messages.get_messages(request)
        storage.used = True
        messages.success(request, '')
        user = authenticate(username=username, password=password)
        print(user)
        if user is not None:
            if user.is_verified:
                print("successful")
                login(request, user)
                return redirect('home')
            else:
                messages.warning(request, 'Please verify your email address to continue to PROJECTO')
        else:
            messages.warning(request, 'Your username or password is wrong! Please provide a valid credentials')
        return render(request, self.template_name, {'username': username, 'password': password})


class SignOutView(View):
    template_name = 'accounts/logout.html'

    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

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
        'full_name': '',
        'batch': '',
        'section': '',
    }

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print("Post method")
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

        if User.objects.filter(email=email).first():
            messages.warning(request, "This email is already in use")
            return render(request, self.template_name, context=self.context)

        if Student.objects.filter(student_id=student_id).first():
            messages.warning(request, "There is already a student with this ID")
            return render(request, self.template_name, context=self.context)

        if password != confirm_password:
            messages.warning(request, "Password and confirm password should be same")
            return render(request, self.template_name, context=self.context)

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password)
        student_profile = Student.objects.create(full_name=full_name, student_id=student_id, batch=batch,
                                                 section=section,
                                                 user_id=user.id)
        if student_profile:
            student_profile.save()
            # email part

            user_id = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user=user)
            token_table_data = Token(user=user, token=token)
            token_table_data.save()
            subject = 'Email Verification of PROJECTO'
            message = f"Hello {full_name}\n\nPlease go to the following link to verify your account.\n\n" \
                      f"{request.build_absolute_uri('account-confirmation/' + user_id + '/' + token)}\n\n" \
                      f"Sincerely," \
                      f"\nYour Projecto Team! "
            from_email = 'homehunt.bd@gmail.com'
            if subject and message and from_email:
                send_registration_email.delay(user_id=user_id, subject=subject, message=message,
                                              email=email)
                messages.success(request,
                                 'Your account has been created, an email will be send shortly. Follow the link to '
                                 'verify your account.')
                return redirect('login')
            else:
                token_table_data.delete()
                return HttpResponse('Make sure all fields are entered and valid.')
        else:
            user.delete()

        return render(request, self.template_name, self.context)


class ProfileView(LoginRequiredMixin, View):
    template_name = 'accounts/profile.html'

    def get(self, request, *args, **kwargs):
        student_profile = Student.objects.filter(user_id=request.user).first()
        teacher_profile = Teacher.objects.filter(user_id=request.user).first()

        print(student_profile)
        print(teacher_profile)

        context = {
            'student': student_profile,
            'teacher': teacher_profile
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        student_profile = Student.objects.filter(user_id=request.user).first()
        teacher_profile = Teacher.objects.filter(user_id=request.user).first()

        if student_profile:
            print(request.POST)
            print(request.POST.get("profile_image"))
            full_name = request.POST.get("full_name")
            student_id = request.POST.get("student_id")
            batch = request.POST.get("batch")
            section = request.POST.get("section")

            storage = messages.get_messages(request)
            storage.used = True
            messages.success(request, '')

            check_student_id = Student.objects.filter(student_id=student_id).first()
            if check_student_id and request.user.student.student_id != check_student_id.student_id:
                messages.warning(request, 'This student id already exists')
            else:
                # student_profile.student_id = student_id
                student_profile.full_name = full_name
                student_profile.batch = batch
                student_profile.section = section
                student_profile.user = request.user
                messages.success(request, "Your profile has been updated.")
                student_profile.save()
                print("Successful")

        else:
            full_name = request.POST.get("full_name")
            initials = request.POST.get("initials")
            email = request.POST.get("email")
            phone = request.POST.get("phone")
            if len(str(phone)) == 0:
                phone = 880
            teacher_profile.full_name = full_name
            teacher_profile.initials = initials
            teacher_profile.email = email
            teacher_profile.phone = phone
            check_teacher = Teacher.objects.filter(initials=initials).first()
            if check_teacher and request.user != check_teacher.user:
                messages.warning(request, "This initials already exists")
            else:
                teacher_profile.save()
                messages.success(request, "Your profile has been updated.")
        context = {
            'student': student_profile,
            'teacher': teacher_profile
        }
        return render(request, self.template_name, context=context)


class TeacherManagementView(SuperUserMixin, View):
    template_name = 'accounts/teacher_management.html'

    def get(self, request, *args, **kwargs):
        context = {
            'teachers': Teacher.objects.exclude(initials='admin')
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        if request.is_ajax():
            print("From ajax")
            delete_button = request.POST.get('delete_teacher')
            if delete_button == 'false':
                checked = request.POST.get('is_checked')
                teacher_id = request.POST.get('teacher_id')
                teacher = Teacher.objects.get(id=teacher_id)
                print(request.user)
                print(teacher.user)
                if checked == 'true':
                    teacher.user.is_superuser = True
                    teacher.user.save()
                    dict = {
                        'alert_type': 'success',
                        'alert_message': teacher.full_name + ' status updated!'
                    }
                else:
                    print(User.objects.filter(is_superuser=True).count())
                    if User.objects.filter(is_superuser=True).count() > 1:
                        teacher.user.is_superuser = False
                        teacher.user.save()
                        if request.user.id == teacher.user.id:
                            dict = {
                                'home': True,
                                'alert_type': 'success',
                                'alert_message': teacher.full_name + ' status updated!'
                            }
                        else:
                            dict = {
                                'alert_type': 'success',
                                'alert_message': teacher.full_name + ' status updated!'
                            }
                    else:
                        dict = {
                            'alert_type': 'warning',
                            'alert_message': 'There must be at least one superuser'
                        }
            else:
                try:
                    teacher_id = request.POST.get('teacher_id')
                    teacher = Teacher.objects.get(id=teacher_id)
                    user = teacher.user
                    teacher.delete()
                    user.delete()
                    dict = {
                        'alert_type': 'success',
                        'alert_message': 'Teacher has been deleted successfully!'
                    }
                except Exception as e:
                    dict = {
                        'alert_type': 'warning',
                        'alert_message': 'Error code 403, failed to delete user'
                    }
            return HttpResponse(json.dumps(dict), content_type='application/json')

        context = {
            'teachers': Teacher.objects.exclude(initials='admin')
        }
        return render(request, self.template_name, context)


class AddTeacherView(SuperUserMixin, View):
    template_name = 'accounts/add_teacher.html'

    def get(self, request, *args, **kwargs):
        context = {
            'username': '',
            'email': '',
            'password': '',
            'confirm_password': '',
            'full_name': '',
            'initials': '',
            'phone': ''
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        full_name = request.POST.get("full_name")
        initials = request.POST.get("initials")
        phone = request.POST.get("phone")
        if len(str(phone)) == 0:
            phone = 880

        context = {
            'username': username,
            'email': email,
            'password': password,
            'confirm_password': confirm_password,
            'full_name': full_name,
            'initials': initials,
            'phone': phone
        }

        if User.objects.filter(username=username).first():
            messages.warning(request, "This username already exists!")
        elif password != confirm_password:
            messages.warning(request, "Password and confirm password should be same")
        else:
            user = User.objects.create_user(username=username, password=password, email=email)
            user.is_verified = True
            user.save()
            teacher = Teacher(full_name=full_name, initials=initials, user=user, email=email, phone=phone)
            teacher.save()
            messages.success(request, full_name + " has been added")

        return render(request, self.template_name, context=context)


class AccountConfirmationView(View):
    template_name = 'accounts/account_confirmation.html'

    def get(self, request, *args, **kwargs):
        token = kwargs['token']
        uid = kwargs['uidb64']

        uid = urlsafe_base64_decode(uid).decode()
        user = User.objects.filter(id=uid).first()

        if not user.is_verified:
            print(user)
            backend_token = Token.objects.filter(user=user).first()
            print(type(backend_token))
            print(type(token))
            if str(backend_token) == token:
                print("Token matched")
                user.is_verified = True
                user.save()
                context = {
                    'success': True,
                    'status': 101
                }
                backend_token.delete()
            else:
                messages.warning(request, "Invalid Link")
                return redirect('login')
        else:
            messages.warning(request, "Your account is already verified. Please Login.")
            return redirect('login')

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, context={})
