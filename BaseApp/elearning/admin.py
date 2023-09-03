from django.contrib import admin
from .models import *
from datetime import timedelta, datetime


class CoursesView(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ('id', 'name', 'subject', 'shortdes')
    list_filter = ["subject", "name"]
    search_fields = ['name']


class LectureView(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ('id', 'name', 'course', 'order')
    list_filter = ["name", "course"]
    search_fields = ['name']


class LectureMaterialView(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ('id', 'name', 'course', 'lecture',
                    'order', 'materialType', 'template')
    list_filter = ["course", 'lecture']
    search_fields = ['name']


class ProgressView(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ('id', 'user', 'CourseName', 'completed', 'completed_on')
    list_filter = ['user']
    search_fields = ['user']

    def CourseName(self, obj):
        return obj.LectureMaterial.course.name


class QuestionsView(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ('id', 'courses', 'question', 'question_type')
    list_filter = ['courses', 'question_type']
    search_fields = ['question']


class QuestionsTakenView(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ('id', 'user', 'courses', 'question',
                    'answerStatus', 'answer', 'created_at')
    list_filter = ['courses', 'answerStatus']
    search_fields = ['question']

    def CourseName(self, obj):
        return obj.LectureMaterial.course.name


class CourseEnrollView(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ('id', 'user', 'courses', 'timedelta',
                    'enrolled_on', 'expireDate')
    list_filter = ['courses', 'user']
    search_fields = ['courses']

    def expireDate(self, obj):
        return obj.enrolled_on + timedelta(days=obj.timedelta)
    
class AnswersView(admin.ModelAdmin):
    # a list of displayed columns name.
    list_display = ('id', 'question', 'answer')
    list_filter = ['question', 'answer']
    search_fields = ['question']

    def expireDate(self, obj):
        return obj.enrolled_on + timedelta(days=obj.timedelta)


# Register your models here.
admin.site.register(UserProfileElearning)
admin.site.register(Subjects)
admin.site.register(Jobs)
admin.site.register(Courses, CoursesView)
admin.site.register(Lecture, LectureView)
admin.site.register(LectureMaterial, LectureMaterialView)
admin.site.register(CourseEnroll, CourseEnrollView)
# admin.site.register(LectureEnroll)
# admin.site.register(LectureMaterialEnroll)
admin.site.register(Questions, QuestionsView)
admin.site.register(QuestionsTaken, QuestionsTakenView)
admin.site.register(Answers,AnswersView)
# admin.site.register(PaymentMethod)
# admin.site.register(Transaction)
admin.site.register(Progress, ProgressView)
admin.site.register(ThemeUI)
admin.site.register(Information)
