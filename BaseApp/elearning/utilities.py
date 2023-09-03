from .models import *
from datetime import timedelta


def getDueDateByCoures(request, course):
    # print(request)
    # print(CourseEnroll.objects.filter(user=request))
    # return ""
    try:
        Course = CourseEnroll.objects.get(user=request, courses=course)
    except:
        return ""
    print(Course.enrolled_on + timedelta(days=Course.timedelta))
    # str(my_datetime)[:19]
    return str(Course.enrolled_on + timedelta(days=Course.timedelta))[:19] + " - Days " + str(Course.timedelta)


def getSingleCourseProgressPerUser(request, course):
    course_letcures = LectureMaterial.objects.filter(course=course)
    print(course_letcures.count())
    course_progress = Progress.objects.filter(
        user=request.user, LectureMaterial__in=course_letcures, completed=True)
    print(course_progress.count())
    return int(course_progress.count() / course_letcures.count() * 100)


def getProgress(request, action,limit):
    print("enter getProgress")
    print("action",action)
    print("limit",limit)
    result = []
    data = {}
    if action == "all":
        print("in action all")
        course_data = Courses.objects.all().order_by('id')[0:int(limit)]
        print("len course_data",len(course_data))
    else:
        # print(CourseEnroll.objects.filter(user=request.user).values('courses'))
        course_data = Courses.objects.filter(id__in=CourseEnroll.objects.filter(user=request.user).values('courses'))

    for Course in course_data:
        data = {}
        data['id'] = Course.id
        data['shortdes'] = Course.shortdes
        data['img'] = str(Course.img.url)
        data['name'] = Course.name
        if CourseEnroll.objects.filter(courses=Course.id, user=request.user.id).exists():
            full_matrial = LectureMaterial.objects.filter(course=Course.id)
            done_matrial = Progress.objects.filter(
                user=request.user, LectureMaterial__in=full_matrial, completed=True)
            try:
                data['progress'] = int(
                    done_matrial.count()/full_matrial.count() * 100)
            except Exception as e:
                data['progress'] = 0
        else:
            data['progress'] = 0
        result.append(data)
    return result


def getLecturesStatus(request, lectures):
    lectures_matrial = LectureMaterial.objects.filter(lecture__in=lectures)
    result = []
    data = {}
    for i in lectures_matrial:
        # print(u.name)
        if Progress.objects.filter(user=request.user, LectureMaterial=i.id, completed=True).exists():
            data['done'] = True
            print("found")
        else:
            data['done'] = False
            print("not found")
        data['name'] = i.name
        result.append(data)
    return result


def updateSingleCourseProgressPerUser(request, lectures):

    if not Progress.objects.filter(user=User.objects.get(id=request), LectureMaterial=LectureMaterial.objects.get(id=lectures), completed=True).exists():
        try:
            progressObject = Progress()
            progressObject.user = User.objects.get(id=request)
            progressObject.LectureMaterial = LectureMaterial.objects.get(
                id=lectures)
            progressObject.completed = True
            progressObject.save()
            print("progress added")
        except Exception as e:
            print("progress failed with " + str(e))
            pass
