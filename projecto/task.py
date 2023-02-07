import datetime
import os

from dateutil.relativedelta import relativedelta
from django.core.mail import send_mail
from django.http import BadHeaderError
from django.utils.http import urlsafe_base64_decode

from accounts.models import User, Student
from project_management.admin import Course
from projecto.celery import app as celery_app


@celery_app.task(name='delete_course')
def delete_course():
    one_yrs_ago = datetime.datetime.now() - relativedelta(years=1)
    courses = Course.objects.filter(
        deadline__range=(
            datetime.date(2000, 1, 1), one_yrs_ago))
    courses.delete()
    return "Course Deleted Successfully"


@celery_app.task(name='send_registration_email')
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


@celery_app.task(name='assigned_supervisor_email')
def assigned_supervisor_email(subject, message, email):
    from_email = os.environ.get('EMAIL_HOST_USER')

    try:
        send_mail(subject, message, from_email, [email])
        return "Email Sent Successfully"
    except BadHeaderError:
        return "Email sending Failed"
