from django import template
from ..models import *
from ..utilities import *
register = template.Library()


@register.simple_tag
def getStatus(user, id,context):
    if context == "matrial":
        if Progress.objects.filter(user=user, LectureMaterial=id,completed=True).exists():
            return 'text-info'
        return "text-dark"

    if context == "question":
        if QuestionsTaken.objects.filter(user=user, question=id).exists():
            return 'text-info'
        return "text-dark"
    
@register.simple_tag
def getProgress(user,courseid):
    return getSingleCourseProgressPerUser(user,courseid)


@register.simple_tag
def getInformation():
    # For footer informations
    return getSingleCourseProgressPerUser(user,courseid)

@register.simple_tag
def GetUI(Tag):
    UI=ThemeUI.objects.all().order_by('id').first()
    if Tag == "navbar_fontSize":
        return UI.navbar_fontSize
    if Tag == "profile_counters":
        return UI.profile_counters
    return ""


@register.simple_tag
def getDueDate(request,courseid):
    # print(user)
    # return " "
    return getDueDateByCoures(request,courseid)
    
