from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.conf import settings
from json import JSONEncoder
from multiprocessing import context
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json
from django.shortcuts import redirect
from django.contrib import messages
from .models import *
from django.views import View
from django.template.loader import render_to_string, get_template
from .utilities import *
import time


def index(request):
    return render(request, 'elearning/index.html', {})


def pagenew(request):
    return render(request, 'workfast/com/base.html', {})
    # return render(request,'workfast/com/login.html',{})


def home(request):
    course=Courses.objects.all()
    return render(request, 'workfast/home.html', {"course":course})


def login_view(request):
    contex = {}
    contex['error'] = False
    if request.user.is_authenticated:
        return HttpResponseRedirect("profile")
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        contex['username'] = username
        contex['password'] = password
        try:
            user = User.objects.get(username=username)
        except:
            print("username 00")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect("profile")
        else:
            contex['error'] = True
            contex['msg'] = "Invalid username or password"
            messages.error(request, "Invalid username or password.")
            return render(request, 'workfast/login.html', {})
    return render(request, 'workfast/login.html', {})


@login_required(login_url="../login/")
def logoutView(request):
    logout(request)
    return HttpResponseRedirect("home")


def SignUp(request):

    context = {}

    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        context['data'] = {"username": username, "email": email}

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            # return redirect('signup')  # Change 'register' to the name of your registration URL pattern.
            return render(request, 'workfast/signup.html', context)

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            # return redirect('signup')
            return render(request, 'workfast/signup.html', context)

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            # return redirect('signup')
            return render(request, 'workfast/signup.html', context)

        # Create the user
        user = User.objects.create_user(
            username=username, email=email, password=password)
        messages.success(
            request, 'Account created successfully. You can now log in.')
        # Change 'login' to the name of your login URL pattern.
        return redirect('login')

    return render(request, 'workfast/signup.html', {})


def forgot_password(request):
    return render(request, 'workfast/forgot-password.html', {})


def account(request):
    return render(request, 'workfast/account.html', {})


@login_required(login_url="login")
def profile(request):
    context = {}
    context['courses'] = getProgress(request, 'none', 0)
    context['Lectures'] = CourseEnroll.objects.filter(
        user=request.user).count()
    context['User'] = User.objects.get(id=request.user.id)
    return render(request, 'workfast/profile.html', context)


def course_details(request, id):
    context = {}

    context['course'] = Courses.objects.get(id=id)
    context['is_enrolled'] = CourseEnroll.objects.filter(
        courses=context['course'], user=request.user).exists()
    print(context['is_enrolled'])

    all_lecture = []

    for i in Lecture.objects.filter(course=context['course']):
        data = {}
        data['course_name'] = i.name
        all_lecture_matrial = []
        for x in LectureMaterial.objects.filter(lecture=i.id):
            data_2 = {}
            data_2['name'] = x.name
            data_2['id'] = x.id
            data_2['done'] = False
            if Progress.objects.filter(user=request.user, LectureMaterial=x.id).exists():
                data_2['done'] = True

            all_lecture_matrial.append(data_2)
            # data['lecture_matrila']=x.name
        data['all_lecture_matrial'] = all_lecture_matrial
        all_lecture.append(data)

    context['all_lecture'] = all_lecture

    # context['LectureMaterial'] = LectureMaterial.objects.filter(lecture__in=context['lectures']).order_by('order')

    return render(request, 'workfast/course-details.html', context)


@login_required(login_url="login")
def course(request):
    context = {}
    context['courses'] = getProgress(request, 'all', 100)
    return render(request, 'workfast/course.html', context)


def course_view(request, id):
    context = {}

    if Courses.objects.filter(id=id).exists():
        course_data = Courses.objects.get(id=id)
    else:
        return render(request, 'workfast/error/course-view-not-found.html', context)

    if not CourseEnroll.objects.filter(user=request.user, courses=id).exists():
        CourseEnrollObject = CourseEnroll()
        CourseEnrollObject.user = request.user
        CourseEnrollObject.courses = Courses.objects.get(id=id)
        CourseEnrollObject.save()

    lecture_data = Lecture.objects.filter(course=course_data).order_by('order')

    LectureMaterial_data = LectureMaterial.objects.filter(
        lecture__in=lecture_data).order_by('order')

    context['course_data'] = course_data
    context['lecture_data'] = lecture_data
    context['LectureMaterial_data'] = LectureMaterial_data

    context['question'] = Questions.objects.filter(courses=course_data)

    return render(request, 'workfast/course-view.html', context)


class course_service(View):

    def get(self, request):

        if is_ajax(request):
            action = request.GET.get('action')
            if action == "getMatrial":
                martialId = request.GET.get('martialId')
                matrial = LectureMaterial.objects.get(id=martialId)
                if matrial.materialType == "TEMPLATE":
                    print("matrial.template", matrial.template)
                    print("martialId", martialId)
                    print("action", action)
                    if "image" in matrial.template:
                        content = render_to_string(
                            'workfast/course-template/image.html', {"test": "sdsdf", "src": matrial.materialFiles.url})
                        return JsonResponse({"content": content}, safe=False)
                    if "video" in matrial.template:
                        content = render_to_string(
                            'workfast/course-template/video.html', {"src": matrial.materialFiles.url})
                        return JsonResponse({"content": content}, safe=False)
                    if "header-text" in matrial.template:
                        content = render_to_string('workfast/course-template/header-text.html', {
                            "value_1": matrial.value_1, "value_2": matrial.value_2})
                        return JsonResponse({"content": content}, safe=False)

            if action == "getQuestion":

                # course = Courses.objects.get(id=request.POST.get('courseId'))
                questionsTotal = Questions.objects.filter(courses=Questions.objects.get(
                    id=request.GET.get('questionId')).courses).count()

                questionsTaken = QuestionsTaken.objects.filter(
                    user=request.user, courses=Questions.objects.get(id=request.GET.get('questionId')).courses).count()
                try:
                    progress=int((questionsTaken/questionsTotal) * 100)
                except Exception as e:
                    progress=0
                try:
                    question = Questions.objects.get(
                        id=request.GET.get('questionId'))
                    answers = Answers.objects.get(question=question)
                    print("action getQuestion")
                    try:
                        question_taken = QuestionsTaken.objects.get(
                            user=request.user, question=question)
                    except Exception as e:
                        question_taken = None
                    if question.question_type == "singlechoices":
                        content = render_to_string('workfast/componants/question-view-singlechoices.html', {
                                                   "question": question, "answers": answers, "question_taken": question_taken,
                                                   'questionsTotal': questionsTotal, 'questionsTaken': questionsTaken,"progress":progress})
                except Exception as e:
                    print(e)
                return JsonResponse({"content": content}, safe=False)

            if action == "getSingleCourseProgressPerUser":
                print("getSingleCourseProgressPerUser")
                courseId = request.GET.get('courseId')
                html = render_to_string(
                    'workfast/com/progress.html', {"progress": getSingleCourseProgressPerUser(request, courseId)})
                return JsonResponse({"content": html})

            if action == "updateSingleCourseProgressPerUser":
                print("updateSingleCourseProgressPerUser")
                updateSingleCourseProgressPerUser(
                    request.GET.get('userId'), request.GET.get('courseId'))

            if action == "getCourse":
                time.sleep(5)
                print("getCourse")
                print(request.GET.get('limit'))
                try:
                    data = getProgress(
                        request, 'all', request.GET.get('limit'))
                    html = render_to_string(
                        'workfast/componants/course-card.html', {"courses": data})
                    return JsonResponse(data={"content": html}, safe=False)
                except Exception as e:
                    print("error")
                    print(e)

        return HttpResponse("Course Service")

    def post(self, request):
        if is_ajax(request):
            action = request.POST.get('action')
            print("POST action", action)
            
            if action == "resetQuestions":
                print(request.POST.get('courseId'))
                print(request.user)
                TakenQuestionByUser=QuestionsTaken.objects.filter(user=request.user,courses=Courses.objects.get(id=request.POST.get('courseId'))
                                              )
                print(TakenQuestionByUser.delete())
                
                return JsonResponse({"status":True},safe=True)
                pass
            if action == "saveQuestionAnswers":
                print("enter ")
                print(request.POST.get('questionid'))
                print(request.user.id)
                print(request.POST.get('answerId'))
                try:
                    QuestionsTaken.objects.filter(user=request.user, question=Questions.objects.get(id=request.POST.get('questionid')),
                                                  courses=Questions.objects.get(id=request.POST.get(
                                                      'questionid')).courses).delete()
                except Exception as e:
                    print(e)
                try:
                    answerStatus = False
                    if request.POST.get('answerId') == Answers.objects.get(question=Questions.objects.get(id=request.POST.get(
                            'questionid'))).answer:
                        answerStatus = True
                    InsertToQuestionTaken = QuestionsTaken(user=request.user, courses=Questions.objects.get(id=request.POST.get(
                        'questionid')).courses, question=Questions.objects.get(id=request.POST.get('questionid')), answer=request.POST.get('answerId'), answerStatus=answerStatus).save()
                except Exception as e:
                    print(e)

            if action == "getResults":

                course = Courses.objects.get(id=request.POST.get('courseId'))
                questions = Questions.objects.filter(courses=course)

                questionsTaken = QuestionsTaken.objects.filter(
                    user=request.user, courses=course)

                TotalQuestions = questionsTaken.count()

                if TotalQuestions == questions.count():
                    status = True
                else:
                    status = False
                    return JsonResponse(data={"status": status}, safe=False)

                print(status)

                CorrectQuestions = questionsTaken.filter(
                    answerStatus=True).count()
                WrongQuestions = questionsTaken.filter(
                    answerStatus=False).count()
                score = (CorrectQuestions/TotalQuestions) * 100

                content = render_to_string(
                    'workfast/componants/results-view.html', {"course": course,
                                                              "TotalQuestions": TotalQuestions,
                                                              "CorrectQuestions": CorrectQuestions,
                                                              "WrongQuestions": WrongQuestions,
                                                              "score": score})

                return JsonResponse(data={"content": content, "status": status}, safe=False)

        return HttpResponse("Course Service")


def is_ajax(request):
    return request.headers.get('x-requested-with') == 'XMLHttpRequest'
