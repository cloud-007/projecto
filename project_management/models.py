import os

from django.db import models
from django.dispatch import receiver
from django.utils.text import gettext_lazy as _

from accounts.models import Student, Teacher


class AbstractTimestampModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class CourseState(models.TextChoices):
    RUNNING = 'RUNNING', _('Running')
    ARCHIVED = 'ARCHIVED', _('Archived')
    UPCOMING = 'UPCOMING', _('Upcoming')
    DELETED = 'DELETED', _('Deleted')


class CourseCodeState(models.TextChoices):
    CSE_3300 = '3300', _('CSE 3300')
    CSE_4800 = '4800', _('CSE 4800')
    CSE_4801 = '4801', _('CSE 4801')


class TitleState(models.TextChoices):
    CSE_3300 = 'CSE 3300', _('Project I')
    CSE_4800 = 'CSE 4800', _('Project II part I')
    CSE_4801 = 'CSE 4801', _('Project II part II')


class Course(AbstractTimestampModel):
    course_code = models.CharField(
        verbose_name=_('Course Code'),
        max_length=32,
        choices=CourseCodeState.choices,
        default=CourseCodeState.CSE_3300
    )

    title = models.CharField(
        verbose_name=_('Title'),
        choices=TitleState.choices,
        max_length=32,
        default="Project I"
    )

    semester = models.CharField(verbose_name=_('Semester'), max_length=32)
    state = models.CharField(
        verbose_name=_('State'),
        max_length=32,
        choices=CourseState.choices,
        default=CourseState.RUNNING
    )
    start_time = models.DateTimeField(verbose_name=_('Start Time'))
    end_time = models.DateTimeField(verbose_name=_('End Time'))

    def __str__(self):
        return self.title


class Proposal(AbstractTimestampModel):
    title = models.CharField(verbose_name=_('Title'), max_length=256)
    course = models.ForeignKey(
        verbose_name=_('Course'),
        to='Course',
        related_name='proposal',
        on_delete=models.CASCADE
    )
    students = models.ManyToManyField(
        verbose_name=_('Students'),
        to='accounts.Student',
        related_name='proposal',
    )

    preferred_supervisors = models.ManyToManyField(
        verbose_name=_('Preferred Supervisor'),
        to='accounts.Teacher',
        related_name='proposals',
    )

    assigned_supervisor = models.ForeignKey(
        verbose_name=_('Assigned Supervisor'),
        to='accounts.Teacher',
        related_name='assigned_proposals',
        null=True,
        on_delete=models.SET_NULL
    )

    assigned_by = models.ForeignKey(
        verbose_name=_('Assigned By'),
        to='accounts.Teacher',
        related_name='+',
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    submitted_by = models.ForeignKey(
        verbose_name=_('Submitted By'),
        to='accounts.Student',
        related_name='proposal_submitted',
        on_delete=models.CASCADE
    )
    team_lead = models.ForeignKey(
        verbose_name=_('Team Lead'),
        to='accounts.Student',
        related_name='+',
        on_delete=models.CASCADE
    )

    file = models.FileField(verbose_name=_('Proposal File'), upload_to='proposals/')

    def __str__(self):
        return self.title


# Deleting proposal file when a proposal gets deleted
@receiver(models.signals.post_delete, sender=Proposal)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MediaFile` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=Proposal)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MediaFile` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = Proposal.objects.get(pk=instance.pk).file
    except Proposal.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Result(AbstractTimestampModel):
    proposal = models.ForeignKey(
        verbose_name=_('Proposal Name'),
        to='Proposal',
        related_name='result',
        on_delete=models.CASCADE
    )
    course = models.ForeignKey(
        verbose_name=_('Course'),
        to='Course',
        related_name='result',
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )
    student = models.ForeignKey(
        verbose_name=_('Student'),
        to='accounts.Student',
        related_name='result',
        on_delete=models.CASCADE
    )

    @property
    def marks(self):
        marksheets = Marksheet.objects.filter(result=self)
        c1 = sum(marksheets.values_list('criteria_1', flat=True))
        c2 = sum(marksheets.values_list('criteria_2', flat=True))
        res = c1 + c2
        res /= max(1, len(marksheets.values_list('criteria_2', flat=True)))
        s_mark = sum(marksheets.values_list('supervisor', flat=True))
        return int(res + s_mark)

    def __str__(self):
        return "CSE - " + str(
            self.proposal.course.course_code) + " | " + self.proposal.course.semester + " | " + self.student.student_id


class Marksheet(AbstractTimestampModel):
    result = models.ForeignKey(
        verbose_name=_('Result'),
        to='project_management.Result',
        related_name='marksheet',
        on_delete=models.CASCADE,
        default=0
    )
    teacher = models.ForeignKey(
        verbose_name=_('Teacher'),
        to='accounts.Teacher',
        related_name='marksheets',
        on_delete=models.CASCADE
    )

    # add marks field
    criteria_1 = models.IntegerField(verbose_name=_('Criteria 1 Mark'))
    criteria_2 = models.IntegerField(verbose_name=_('Criteria 2 Mark'))
    supervisor = models.IntegerField(verbose_name=_('Supervisor Mark'))

    def __str__(self):
        return self.result.proposal.title + " - " + self.result.student.student_id


class Notice(AbstractTimestampModel):
    title = models.CharField(verbose_name=_('Title'), max_length=256)
    description = models.TextField(verbose_name=_('Description'))
    course_code = models.CharField(
        verbose_name=_('Course Code'),
        max_length=32,
        choices=CourseCodeState.choices,
        default=CourseCodeState.CSE_3300
    )
    semester = models.CharField(verbose_name=_('Semester'), max_length=32, blank=True)

    def __str__(self):
        return self.title
