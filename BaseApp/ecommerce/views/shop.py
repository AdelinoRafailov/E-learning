from django.shortcuts import render
from ..models import *
from django.views import View

def shophome(request):

    return render(request,'ecommerce/shop-grid.html',{})
