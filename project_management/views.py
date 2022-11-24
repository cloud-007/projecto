import datetime
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View

from accounts.models import Teacher, Student
from project_management.mixins import TeacherRequiredMixin, SuperUserMixin
from project_management.models import Course, Proposal, Result, Marksheet


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):
        running_courses = Course.objects.filter(
            deadline__range=(datetime.datetime.now().date(), datetime.date(2500, 1, 1))).order_by('deadline')
        archived_courses = Course.objects.filter(
            deadline__range=(
                datetime.date(2000, 1, 1), datetime.datetime.now().date() - datetime.timedelta(1))).order_by('deadline')

        return render(request, self.template_name,
                      {'courses': running_courses, 'archived': archived_courses})


class ProjectDetailsView(TeacherRequiredMixin, View):
    template_name = 'project_management/project_details.html'

    context = {
        'course': Course(),
        'proposals': Proposal(),
        'filter_by': 'all',
        'teachers': Teacher.objects.all()
    }

    def get(self, request, *args, **kwargs):
        print(args)
        print(kwargs)
        course_id = kwargs.get('id')
        print(course_id)
        course = Course.objects.get(id=course_id)
        filter_by = kwargs.get('filter_by')

        if filter_by == 'all':
            proposals = course.proposal_set.all()
        elif filter_by == 'assigned':
            proposals = course.proposal_set.filter(assigned_supervisor__isnull=False)
        elif filter_by == request.user.teacher.initials:
            proposals = course.proposal_set.filter(assigned_supervisor=request.user.teacher)
        else:
            proposals = course.proposal_set.filter(assigned_supervisor__isnull=True)

        print(proposals)
        print(len(proposals.values_list('students', flat=True)))

        print(course)
        self.context = {
            'course': course,
            'proposals': proposals,
            'student_count': len(proposals.values_list('students', flat=True)),
            'filter_by': filter_by,
            'teachers': Teacher.objects.all()
        }

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        # check if it is an ajax call
        if request.is_ajax() and request.user.is_staff:
            print("Came from ajax")
            delete_proposal = request.POST.get("delete_button")
            print(delete_proposal)

            proposal_id = request.POST.get("proposal_id")
            proposal = Proposal.objects.get(id=proposal_id)
            # if the admin is requesting to delete the proposal
            if delete_proposal == 'true':
                proposal.delete()
            # otherwise he is trying to assign a supervisor
            else:
                print("Assign Supervisor")
                proposal.assigned_supervisor = Teacher.objects.get(id=request.POST.get("teacher_id"))
                proposal.assigned_by = request.user.teacher
                proposal.save()
                print(proposal.assigned_supervisor)

            course_id = kwargs.get('id')
            course = Course.objects.get(id=course_id)
            filter_by = kwargs.get('filter_by')
            if filter_by == 'all':
                proposals = course.proposal_set.all()
            elif filter_by == 'assigned':
                proposals = course.proposal_set.filter(assigned_supervisor__isnull=False)
            else:
                proposals = course.proposal_set.filter(assigned_supervisor__isnull=True)
            self.context = {
                'course': course,
                'proposals': proposals,
                'filter_by': filter_by,
                'teachers': Teacher.objects.all()
            }

        return render(request, self.template_name, self.context)


class CreateNewCourse(SuperUserMixin, View):
    template_name = 'project_management/create_new_course.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {})

    def post(self, request, *args, **kwargs):
        print(request.POST)
        course = Course()
        code = request.POST.get("course_code")
        val = code.split(" ")
        course.course_id = val[1]
        course.title = request.POST.get("course_title")
        course.semester = request.POST.get("semester")
        course.deadline = request.POST.get("deadline")

        context = {
            'course': course
        }

        if Course.objects.filter(course_id=course.course_id, semester=course.semester).first():
            messages.warning(request, "This course for this semester already exists")
            return render(request, self.template_name, context=context)

        course.save()
        messages.success(request, course.title + " has been added successfully")

        return redirect('home')


class UpdateCourseView(SuperUserMixin, View):
    template_name = 'project_management/update_course_view.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        course = Course.objects.get(id=pk)
        context = {
            'course': course
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        course = Course.objects.get(id=pk)

        print(request.POST)
        print("Submit")
        print(request.POST.get("submit_button"))
        print("Delete")
        print(request.POST.get("delete_button"))

        if request.POST.get("submit_button") is None:
            course.delete()
            messages.success(request, course.title + " deleted successfully")
            return redirect('home')
        print("Updating course")
        code = request.POST.get("course_code")
        val = code.split(" ")
        if Course.objects.filter(course_id=val[1], semester=request.POST.get("semester")).first():
            messages.warning(request, "There is already a course for this semester")
            context = {
                'course': course
            }
        else:
            course.course_id = val[1]
            course.title = request.POST.get("course_title")
            course.semester = request.POST.get("semester")
            course.deadline = request.POST.get("deadline")
            course.save()
            context = {
                'course': Course.objects.get(id=pk)
            }

            messages.success(request, course.title + " updated successfully")

        return render(request, self.template_name, context=context)


class ProposalSubmissionView(LoginRequiredMixin, View):
    template_name = 'project_management/proposal_submission.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        course = Course.objects.get(id=pk)
        proposal = Proposal.objects.filter(students=request.user.student, course_id=course.id).first()

        context = {
            'students': Student.objects.exclude(proposal__course=course),
            'teachers': Teacher.objects.all(),
            'proposal': proposal
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        print(request.POST)
        pk = kwargs.get('id')
        course = Course.objects.get(id=pk)

        proposal = Proposal()

        proposal.title = request.POST.get("title")
        proposal.course = course
        proposal.submitted_by = request.user.student
        proposal.team_lead = request.user.student
        proposal.file = request.FILES['proposal_file']
        print(proposal.file)
        proposal.save()
        student_list = []

        for student in json.loads(request.POST.get("tagify_student")):
            student_list.append(student['value'])

        students = Student.objects.filter(student_id__in=student_list)

        for student in students:
            result = Result(proposal=proposal, student=student)
            result.save()

        proposal.students.set(students)

        teacher_list = []

        for teacher in json.loads(request.POST.get("tagify_teacher")):
            teacher_list.append(teacher['value'])
        teachers = Teacher.objects.filter(full_name__in=teacher_list)
        proposal.preferred_supervisors.set(teachers)

        messages.success(request, "Your response has been recorded")

        proposal.save()

        return redirect('home')


class ProposalUpdateView(SuperUserMixin, View):
    template_name = 'project_management/proposal_update.html'

    def get(self, request, *args, **kwargs):
        pk = kwargs.get('id')
        course = Course.objects.get(id=pk)
        proposal_id = kwargs.get('proposal_id')
        proposal = Proposal.objects.get(id=proposal_id)

        context = {
            'students': Student.objects.exclude(proposal__course=course),
            'teachers': Teacher.objects.all(),
            'proposal': proposal
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):

        proposal = Proposal.objects.get(id=kwargs.get('proposal_id'))

        proposal.title = request.POST.get("title")
        print(proposal.file)
        proposal.save()
        student_list = []

        for student in json.loads(request.POST.get("tagify_student")):
            student_list.append(student['value'])

        students = Student.objects.filter(student_id__in=student_list)
        proposal.students.set(students)

        teacher_list = []

        for teacher in json.loads(request.POST.get("tagify_teacher")):
            teacher_list.append(teacher['value'])
        teachers = Teacher.objects.filter(full_name__in=teacher_list)
        proposal.preferred_supervisors.set(teachers)

        messages.success(request, "Proposal has been updated")

        proposal.save()

        context = {
            'students': Student.objects.exclude(proposal__course=proposal.course),
            'teachers': Teacher.objects.all(),
            'proposal': proposal
        }

        return render(request, self.template_name, context=context)


class MarkingStudentView(TeacherRequiredMixin, View):
    template_name = 'project_management/marking_student.html'

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('id')
        proposal_id = kwargs.get('proposal_id')
        course = Course.objects.get(id=course_id)
        proposal = Proposal.objects.get(id=proposal_id)
        context = {
            'course': course,
            'proposal': proposal
        }
        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        print(request.POST)

        course_id = kwargs.get('id')
        proposal_id = kwargs.get('proposal_id')
        course = Course.objects.get(id=course_id)
        proposal = Proposal.objects.get(id=proposal_id)

        full_marks = request.POST.get('full_marks')
        criteria1 = request.POST.get('criteria1')
        is_absent = request.POST.get('isAbsent')

        # marking the student one by one
        if len(str(full_marks)) == 0 and len(str(criteria1)) == 0 and is_absent is None:
            for student in proposal.students.all():
                full_marks = request.POST.get('full_marks' + student.student_id)
                criteria1 = request.POST.get('criteria1' + student.student_id)
                criteria2 = request.POST.get('criteria2' + student.student_id)
                detailed_marking = request.POST.get('detailed_marking' + student.student_id)
                s_mark = request.POST.get('supervisor_mark' + student.student_id)
                is_absent = request.POST.get('isAbsent' + student.student_id)
                print('full marks ' + str(full_marks))
                print('criteria1 ' + str(criteria1))
                print('criteria2 ' + str(criteria2))
                print('detailed_marking ' + str(detailed_marking))
                # if student is not absent create a marksheet for him
                if is_absent is None:
                    # id detailed marking is none, then set criteria1 = full marks, criteria2 = 0
                    if detailed_marking is None:
                        criteria1 = full_marks
                        criteria2 = 0
                    if len(str(s_mark)) == 0:
                        supervisor_mark = 0
                    else:
                        supervisor_mark = s_mark
                    marksheet = Marksheet.objects.filter(result__proposal=proposal,
                                                         result__student=student,
                                                         teacher=request.user.teacher).first()
                    if marksheet is None:
                        marksheet = Marksheet(
                            result=proposal.result.get(student=student),
                            teacher=request.user.teacher,
                            criteria_1=criteria1,
                            criteria_2=criteria2,
                            supervisor=supervisor_mark
                        )
                        marksheet.save()
                    else:
                        marksheet.criteria_1 = int(criteria1)
                        marksheet.criteria_2 = int(criteria2)
                        marksheet.supervisor = int(supervisor_mark)
                        marksheet.save()
                # set his previous marks to zero if any
                else:
                    marksheet = Marksheet.objects.filter(result__proposal=proposal,
                                                         result__student=student,
                                                         teacher=request.user.teacher).first()
                    if marksheet:
                        marksheet.criteria_1 = 0
                        marksheet.criteria_2 = 0
                        marksheet.supervisor = 0
                        marksheet.save()
        else:
            # if everyone is absent don't create any marksheet
            if is_absent == 'on':
                # set zero in his marksheet
                for student in proposal.students.all():
                    marksheet = Marksheet.objects.filter(result__proposal=proposal,
                                                         result__student=student,
                                                         teacher=request.user.teacher).first()
                    if marksheet:
                        marksheet.criteria_1 = 0
                        marksheet.criteria_2 = 0
                        marksheet.supervisor = 0
                        marksheet.save()

            # otherwise create a marksheet for every student
            else:
                # marked in details
                if len(str(full_marks)) == 0:
                    criteria1 = request.POST.get('criteria1')
                    criteria2 = request.POST.get('criteria2')
                # marked in full marks
                else:
                    full_marks = request.POST.get('full_marks')
                    criteria1 = full_marks
                    criteria2 = 0
                s_mark = request.POST.get('supervisor_mark')
                # check supervisor mark
                if len(str(s_mark)) == 0:
                    supervisor_mark = 0
                else:
                    supervisor_mark = request.POST.get('supervisor_mark')

                # update student marksheet for this proposal
                for student in proposal.students.all():
                    marksheet = Marksheet.objects.filter(result__proposal=proposal,
                                                         result__student=student,
                                                         teacher=request.user.teacher).first()
                    if marksheet:
                        marksheet.criteria_1 = int(criteria1)
                        marksheet.criteria_2 = int(criteria2)
                        marksheet.supervisor = int(supervisor_mark)
                        marksheet.save()
                    else:
                        marksheet = Marksheet(
                            result=proposal.result.get(student=student),
                            teacher=request.user.teacher,
                            criteria_1=criteria1,
                            criteria_2=criteria2,
                            supervisor=supervisor_mark
                        )
                        marksheet.save()

        messages.success(request, "Marking successful")
        context = {
            'course': course,
            'proposal': proposal
        }

        return render(request, self.template_name, context=context)


class ResultSheetView(SuperUserMixin, View):
    template_name = 'project_management/course_results.html'

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('id')
        course = Course.objects.get(id=course_id)
        marks = Result.objects.filter(proposal__in=course.proposal_set.all())
        print(marks)
        context = {
            'marks': marks
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})
