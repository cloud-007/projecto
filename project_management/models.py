from django.db import models
from django.utils.text import gettext_lazy as _

from accounts.models import Student, Teacher


class AbstractTimestampModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-id']


class Course(AbstractTimestampModel):
    course_id = models.IntegerField(verbose_name=_('Course ID'))
    title = models.CharField(verbose_name=_('Course Title'), max_length=64)
    semester = models.CharField(verbose_name=_('Semester'), max_length=32)
    deadline = models.DateField(verbose_name=_('Deadline'))

    def __str__(self):
        return self.title


class Proposal(AbstractTimestampModel):
    title = models.CharField(verbose_name=_('Title'), max_length=256)
    course = models.ForeignKey(Course, on_delete=models.PROTECT)
    students = models.ManyToManyField(
        verbose_name=_('Students'),
        to='accounts.Student',
        related_name='proposal',
    )
    # preferred_supervisors = models.CharField(verbose_name=_('Preferred Supervisor'), max_length=128)
    preferred_supervisors = models.ManyToManyField(
        verbose_name=_('Preferred Supervisor'),
        to='accounts.Teacher',
        related_name='proposals',
    )
    # assigned_supervisor = models.ForeignKey(Teacher)
    assigned_supervisor = models.ForeignKey(
        verbose_name=_('Assigned Supervisor'),
        to='accounts.Teacher',
        related_name='assigned_proposals',
        null=True,
        on_delete=models.PROTECT
    )
    # assigned_by = models.CharField(verbose_name=_('Assigned By'), max_length=16)
    assigned_by = models.ForeignKey(
        verbose_name=_('Assigned By'),
        to='accounts.Teacher',
        related_name='+',
        on_delete=models.PROTECT,
        null=True,
        blank=True
    )
    # submitted_by = models.CharField(verbose_name=_('Submitted By'), max_length=32)
    submitted_by = models.ForeignKey(
        verbose_name=_('Submitted By'),
        to='accounts.Student',
        related_name='proposal_submitted',
        on_delete=models.PROTECT
    )
    team_lead = models.ForeignKey(
        verbose_name=_('Team Lead'),
        to='accounts.Student',
        related_name='+',
        on_delete=models.PROTECT
    )

    file = models.FileField(upload_to='proposals/')

    def __str__(self):
        return self.title


class Result(AbstractTimestampModel):
    proposal = models.ForeignKey(
        verbose_name=_('Proposal Name'),
        to='Proposal',
        related_name='result',
        on_delete=models.PROTECT
    )
    student = models.ForeignKey(
        verbose_name=_('Student'),
        to='accounts.Student',
        related_name='result',
        on_delete=models.PROTECT
    )
    marks = models.FloatField(
        verbose_name=_('Total Marks'),
        max_length=32
    )

    def __str__(self):
        return self.proposal.proposal_id


class Marksheet(AbstractTimestampModel):
    proposal = models.ForeignKey(
        verbose_name=_('Proposals'),
        to='Proposal',
        related_name='marksheets',
        on_delete=models.PROTECT
    )
    student = models.ForeignKey(
        verbose_name=_('Student'),
        to='accounts.Student',
        related_name='marksheets',
        on_delete=models.PROTECT
    )
    teacher = models.ForeignKey(
        verbose_name=_('Teacher'),
        to='accounts.Teacher',
        related_name='marksheets',
        on_delete=models.PROTECT
    )

    # add marks field
    criteria_1 = models.FloatField(verbose_name=_('Criteria 1 Mark'), max_length=128)
    criteria_2 = models.FloatField(verbose_name=_('Criteria 2 Mark'), max_length=128)
    supervisor = models.FloatField(verbose_name=_('Supervisor Mark'), max_length=128)

    def __str__(self):
        return self.proposal.title
