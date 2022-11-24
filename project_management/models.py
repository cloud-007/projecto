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
        on_delete=models.CASCADE
    )
    student = models.ForeignKey(
        verbose_name=_('Student'),
        to='accounts.Student',
        related_name='result',
        on_delete=models.PROTECT
    )

    @property
    def marks(self):
        marksheets = Marksheet.objects.filter(result=self)
        c1 = sum(marksheets.values_list('criteria_1', flat=True)) / len(marksheets.values_list('criteria_1', flat=True))
        c2 = sum(marksheets.values_list('criteria_2', flat=True)) / len(marksheets.values_list('criteria_2', flat=True))
        s_mark = sum(marksheets.values_list('supervisor', flat=True))
        return c1 + c2 + s_mark

    def __str__(self):
        return self.student.student_id


class Marksheet(AbstractTimestampModel):
    result = models.ForeignKey(
        verbose_name=_('Result'),
        to='Result',
        related_name='marksheets',
        on_delete=models.CASCADE,
        default=0
    )
    teacher = models.ForeignKey(
        verbose_name=_('Teacher'),
        to='accounts.Teacher',
        related_name='marksheets',
        on_delete=models.PROTECT
    )

    # add marks field
    criteria_1 = models.IntegerField(verbose_name=_('Criteria 1 Mark'))
    criteria_2 = models.IntegerField(verbose_name=_('Criteria 2 Mark'))
    supervisor = models.IntegerField(verbose_name=_('Supervisor Mark'))

    def __str__(self):
        return self.result.proposal.title + " - " + self.result.student.student_id
