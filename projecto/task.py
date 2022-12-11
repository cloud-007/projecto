import os

from django.core.mail import send_mail
from django.http import BadHeaderError
from django.utils.http import urlsafe_base64_decode

from accounts.models import User, Student
from projecto.celery import app


@app.task(name='test')
def test_function():
    print("Say Hello in every thirty seconds")
    return "Done"


@app.task(name='send_registration_email')
def send_registration_email(user_id, subject, message, email):
    print("Hello from send email in celery")
    uid = urlsafe_base64_decode(user_id).decode()
    user = User.objects.filter(id=uid).first()
    student_profile = Student.objects.get(user=user)

    from_email = os.environ.get('EMAIL_HOST_USER')

    print(user)
    print(student_profile)

    try:
        send_mail(subject, message, from_email, [email])
        return "Email Sent Successfully"
    except BadHeaderError:
        print("Exception Found")
        student_profile.delete()
        user.delete()
        return "Email sending Failed"


@app.task(name='assigned_supervisor_email')
def assigned_supervisor_email(subject, message, email):
    from_email = os.environ.get('EMAIL_HOST_USER')

    try:
        send_mail(subject, message, from_email, [email])
        return "Email Sent Successfully"
    except BadHeaderError:
        return "Email sending Failed"
