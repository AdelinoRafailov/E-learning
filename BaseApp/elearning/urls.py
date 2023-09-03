from django.urls import path
from .views import *

urlpatterns = [
    path('', home),
    
    path('newpage',pagenew),
    
    path('home',home,name="home"),
    
    path('course',course,name="course"),
    
    path('login',login_view,name="login"),
    
    path('logout',logoutView,name="logout"),
    
    path('signup',SignUp,name="signup"),
    
    path('course-details/<int:id>',course_details,name="course_details"),
    
    path('course-view/<int:id>',course_view,name="course_view"),
    
    path('course_service',course_service.as_view(),name="course_service"),
    
    path('forgot_password',forgot_password,name="forgot_password"),
    
    
    path('account',account,name="account"),
    
    path('profile',profile,name="profile"),
]