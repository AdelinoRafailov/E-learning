from django.shortcuts import render
from ..models import *
from django.views import View


# get_or_create

def index(request):
    return render(request, 'ecommerce/core/base.html', {})

