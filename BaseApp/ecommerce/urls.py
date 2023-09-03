from django.urls import path
from .views import *

urlpatterns = [
    path('', index),
    path('home/', home, name="home"),
    path('product/<str:uid>',  productView.as_view(), name="product"),
    path('shop/',  shophome, name="shop"),
]