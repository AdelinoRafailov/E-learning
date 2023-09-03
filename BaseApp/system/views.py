from django.http import HttpResponse
from django.shortcuts import render
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from .models import AppDetails




def loginView(request):
    return HttpResponse("test")

# Create your views here.
def settings(request):
    context={}
    context['settings']=AppDetails.AppDetails_Get()

    if request.method == "POST":
        try:
            print("POST_________")
            name=request.POST['name']
            logo = request.FILES['logo']
            fs = FileSystemStorage()
            filename = fs.save(logo.name, logo)
            uploaded_file_url = fs.url(filename)
            AppDetails.AppDetails_Save(name,uploaded_file_url,request.user)
        except Exception as e:
            print("Error")
            return HttpResponse(e)
    return render(request,'system/settings.html',context)