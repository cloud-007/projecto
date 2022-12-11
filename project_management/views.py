import csv
import datetime
import json

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.loader import get_template
from django.views import View
from xhtml2pdf import pisa

from accounts.models import Teacher, Student
from project_management.mixins import TeacherRequiredMixin, SuperUserMixin
from project_management.models import Course, Proposal, Result, Marksheet


class HomeView(View):
    template_name = 'home.html'

    def get(self, request, *args, **kwargs):

        cur_date = datetime.datetime.now().date()

        if cur_date.month <= 6:
            semester = "Spring " + str(cur_date.year)
        else:
            semester = "Summer " + str(cur_date.year)

        running_courses = Course.objects.filter(semester=semester,
                                                deadline__range=(
                                                    datetime.datetime.now().date(),
                                                    datetime.date(2500, 1, 1))).order_by(
            'deadline')
        archived_courses = Course.objects.filter(
            deadline__range=(
                datetime.date(2000, 1, 1), datetime.datetime.now().date() - datetime.timedelta(1))).order_by('deadline')

        try:
            course_list = request.user.student.proposal.values_list('course', flat=True)
        except (Exception,) as e:
            course_list = None
        context = {
            'courses': running_courses,
            'archived': archived_courses,
            'course_list': course_list
        }

        return render(request, self.template_name, context)


class ProjectDetailsView(TeacherRequiredMixin, View):
    template_name = 'project_management/project_details.html'

    context = {
        'course': Course(),
        'proposals': Proposal(),
        'filter_by': 'all',
        'teachers': Teacher.objects.exclude(initials="admin")
    }

    def get(self, request, *args, **kwargs):
        course_id = kwargs.get('id')
        query = request.GET.get('query')
        print("Printing from submission page")
        print(course_id)
        course = Course.objects.get(id=course_id)
        filter_by = kwargs.get('filter_by')

        if filter_by == 'all':
            proposals = course.proposal.all()
        elif filter_by == 'assigned':
            proposals = course.proposal.filter(assigned_supervisor__isnull=False)
        elif filter_by == request.user.teacher.initials:
            proposals = course.proposal.filter(assigned_supervisor=request.user.teacher)
        else:
            proposals = course.proposal.filter(assigned_supervisor__isnull=True)
        if query:
            proposals = proposals.filter(students__student_id=query)

        if request.is_ajax():
            print("This is ajax call to download all pdf")
            type = request.GET.get("type", None)
            if type == "PDF":
                print("Downloading Submission of proposals")
                data = {
                    'course': course,
                    'proposals': proposals,
                    'filter_by': filter_by,
                    'teachers': Teacher.objects.exclude(initials="admin")
                }

                template = get_template('project_management/download_proposal_list_pdf.html')
                html = template.render(data)

                file = open('test.pdf', "w+b")
                pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                            encoding='utf-8')
                file.seek(0)
                pdf = file.read()
                file.close()
                return HttpResponse(pdf, 'application/pdf')

        print(course)
        self.context = {
            'course': course,
            'proposals': proposals,
            'student_count': len(proposals.values_list('students', flat=True)),
            'filter_by': filter_by,
            'teachers': Teacher.objects.exclude(initials="admin")
        }

        return render(request, self.template_name, self.context)

    def post(self, request, *args, **kwargs):
        # check if it is an ajax call
        course_id = kwargs.get('id')
        print(course_id)
        course = Course.objects.get(id=course_id)
        filter_by = kwargs.get('filter_by')
        if filter_by == 'all':
            proposals = course.proposal.all()
        elif filter_by == 'assigned':
            proposals = course.proposal.filter(assigned_supervisor__isnull=False)
        else:
            proposals = course.proposal.filter(assigned_supervisor__isnull=True)
        self.context = {
            'course': course,
            'proposals': proposals,
            'filter_by': filter_by,
            'teachers': Teacher.objects.exclude(initials="admin")
        }
        if request.is_ajax() and request.user.is_superuser:

            print("Came from ajax")
            delete_proposal = request.POST.get("delete_button")
            print(delete_proposal)
            proposal_id = request.POST.get("proposal_id")
            proposal = Proposal.objects.get(id=proposal_id)
            # if the admin is requesting to delete the proposal
            if proposal.course.course_id == 4800:
                sem = proposal.course.semester.split(" ")
                semester = sem[0]
                year = sem[1]
                if semester == "Spring":
                    next_semester = "Summer"
                    next_year = year
                else:
                    next_semester = "Spring"
                    next_year = int(year) + 1
                next_semester = next_semester + " " + str(next_year)
                next_proposal = Proposal.objects.get(
                    course=Course.objects.get(course_id=4801, semester=next_semester),
                    team_lead=proposal.team_lead)
            else:
                next_proposal = None
            if delete_proposal == 'true':
                proposal.delete()
                if next_proposal:
                    next_proposal.delete()
            # otherwise he is trying to assign a supervisor
            else:
                print("Assign Supervisor")
                proposal.assigned_supervisor = Teacher.objects.get(id=request.POST.get("teacher_id"))
                proposal.assigned_by = request.user.teacher
                proposal.save()
                if next_proposal:
                    next_proposal.assigned_supervisor = proposal.assigned_supervisor
                    next_proposal.assigned_by = request.user.teacher
                    next_proposal.save()
                print(proposal.assigned_supervisor)

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
        print(type(course.course_id))
        if course.course_id == "4800":
            sem = course.semester.split(" ")
            semester = sem[0]
            year = sem[1]
            if semester == "Spring":
                next_semester = "Summer"
                next_year = year
                deadline = datetime.datetime(int(next_year), 12, 31)
            else:
                next_semester = "Spring"
                next_year = int(year) + 1
                deadline = datetime.datetime(int(next_year), 6, 30)
            next_semester = next_semester + " " + str(next_year)
            if Course.objects.filter(course_id=4801, semester=next_semester).first():
                pass
            else:
                course = Course(course_id=4801, title="Project 2 part ii", semester=next_semester,
                                deadline=deadline)
                course.save()
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
        check_course = Course.objects.filter(course_id=val[1], semester=request.POST.get("semester")).first()
        if check_course is not None and (
                check_course.course_id != course.course_id or check_course.semester != course.semester):
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
            'teachers': Teacher.objects.exclude(initials="admin"),
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
            result = Result(proposal=proposal, course=course, student=student)
            result.save()

        proposal.students.set(students)

        teacher_list = []

        for teacher in json.loads(request.POST.get("tagify_teacher")):
            teacher_list.append(teacher['value'])
        teachers = Teacher.objects.filter(full_name__in=teacher_list)
        proposal.preferred_supervisors.set(teachers)

        messages.success(request, "Your response has been recorded")

        proposal.save()
        print(proposal.course.course_id)
        if proposal.course.course_id == 4800:
            print("Creating new proposal for 4801")

            sem = proposal.course.semester
            sem = sem.split(" ")
            semester = sem[0]
            year = sem[1]
            if semester == "Spring":
                next_semester = "Summer"
                next_year = year
            else:
                next_semester = "Spring"
                next_year = int(year) + 1

            semester = str(next_semester) + " " + str(next_year)
            print(course)
            print(semester)

            new_proposal = proposal
            new_proposal.id = None
            new_proposal.file = request.FILES['proposal_file']
            new_proposal.course = Course.objects.get(course_id=4801, semester=semester)
            new_proposal.save()
            print(new_proposal)
            new_proposal.students.set(students),
            new_proposal.preferred_supervisors.set(teachers),

            new_proposal.save()

            for student in students:
                result = Result(proposal=new_proposal, course=new_proposal.course, student=student)
                result.save()

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
            'teachers': Teacher.objects.exclude(initials="admin"),
            'proposal': proposal
        }

        return render(request, self.template_name, context=context)

    def post(self, request, *args, **kwargs):
        proposal = Proposal.objects.get(id=kwargs.get('proposal_id'))
        if proposal.course.course_id == 4800:
            sem = proposal.course.semester.split(" ")
            semester = sem[0]
            year = sem[1]
            if semester == "Spring":
                next_semester = "Summer"
                next_year = year
            else:
                next_semester = "Spring"
                next_year = int(year) + 1
            next_semester = next_semester + " " + str(next_year)
            next_proposal = Proposal.objects.get(course=Course.objects.get(course_id=4801, semester=next_semester),
                                                 team_lead=proposal.team_lead)
        else:
            next_proposal = None

        print("Check the file attribute")
        print(request.FILES.get('proposal_file', None))

        '''Removing results of previously set student'''
        for student in proposal.students.all():
            result = Result.objects.get(proposal=proposal, course=proposal.course, student=student)
            result.delete()

        if next_proposal:
            '''Removing results of previously set student of 4801'''
            for student in next_proposal.students.all():
                result = Result.objects.get(proposal=next_proposal, course=next_proposal.course, student=student)
                result.delete()

        proposal.title = request.POST.get("title")
        if request.FILES.get('proposal_file', None):
            proposal.file = request.FILES.get('proposal_file', None)
        print(proposal.file)
        proposal.save()
        student_list = []

        for student in json.loads(request.POST.get("tagify_student")):
            student_list.append(student['value'])

        students = Student.objects.filter(student_id__in=student_list)
        proposal.students.set(students)

        if next_proposal:
            if request.FILES.get('proposal_file', None):
                next_proposal.file = request.FILES.get('proposal_file', None)
            next_proposal.students.set(students)

        '''Add resultsheet for the updated student'''
        for student in students:
            result = Result(proposal=proposal, course=proposal.course, student=student)
            result.save()

        '''Add resultsheet for 4801 if the course is 4800'''
        if next_proposal:
            for student in students:
                result = Result(proposal=next_proposal, course=next_proposal.course, student=student)
                result.save()

        teacher_list = []

        for teacher in json.loads(request.POST.get("tagify_teacher")):
            teacher_list.append(teacher['value'])
        teachers = Teacher.objects.filter(full_name__in=teacher_list)

        proposal.preferred_supervisors.set(teachers)
        if next_proposal:
            next_proposal.preferred_supervisors.set(teachers)

        messages.success(request, "Proposal has been updated")

        proposal.save()
        if next_proposal:
            next_proposal.save()

        context = {
            'students': Student.objects.exclude(proposal__course=proposal.course),
            'teachers': Teacher.objects.exclude(initials="admin"),
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
        if request.is_ajax():
            print(request.GET.get('student_id'))
            print(request.user.teacher)
            result = Marksheet.objects.filter(teacher=request.user.teacher,
                                              result__proposal=proposal,
                                              result__student__student_id=request.GET.get('student_id'))
            print("Printing serialized data")
            print(serializers.serialize("json", result))
            dict = {
                'result': serializers.serialize("json", result),
            }
            return HttpResponse(json.dumps(dict), content_type='application/json')
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
        print("Printing query")
        print(course_id)
        if course_id == 594612:
            print("I am inside query")
            cur_date = datetime.datetime.now().date()

            if cur_date.month <= 6:
                semester = "Spring " + str(cur_date.year)
            else:
                semester = "Summer " + str(cur_date.year)

            running_courses = Course.objects.filter(semester=semester,
                                                    deadline__range=(
                                                        datetime.datetime.now().date(),
                                                        datetime.date(2500, 1, 1))).order_by(
                'deadline')
            results = Result.objects.filter(course__in=running_courses.all())
            course = Course(id=594612)
        else:
            course = Course.objects.get(id=course_id)
            results = Result.objects.filter(proposal__in=course.proposal.all())
        if request.is_ajax():
            print("This is an ajax call")
            print(request.GET)
            type = request.GET.get("type", None)
            if type == 'CSV':
                print("This is csv file download request")
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = 'attachment; filename=Result '

                writer = csv.writer(response)
                writer.writerow(['Name', 'ID', 'Marks', 'Date'])

                for result in results:
                    writer.writerow(
                        [result.student.full_name, result.student.student_id, result.marks, result.created_date])
                print(response)
                return response
            else:
                print("From pdf button")
                data = {
                    'results': results,
                    'course': course
                }

                template = get_template('project_management/download_course_result_pdf.html')
                html = template.render(data)

                file = open('test.pdf', "w+b")
                pisaStatus = pisa.CreatePDF(html.encode('utf-8'), dest=file,
                                            encoding='utf-8')
                file.seek(0)
                pdf = file.read()
                file.close()
                return HttpResponse(pdf, 'application/pdf')

        print(results)
        context = {
            'results': results,
            'course': course
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        return render(request, self.template_name, {})


def test(request):
    return HttpResponse("Done")
