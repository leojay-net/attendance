from django.urls import path
from .views import (StudentLoginView, StudentLogoutView, StudentRegisterView,
                    StudentProfileCreateView, StudentProfilesView, StudentProfileView,
                    StudentActivationView)

urlpatterns = [
    path('student/register', StudentRegisterView.as_view(), name='student_register'),
    path('student/login', StudentLoginView.as_view(), name='student_login'),
    path('student/logout', StudentLogoutView.as_view(), name='student_logout'),
    path('student/create/profile', StudentProfileCreateView.as_view(), name='student_create_profile'),
    path('student/profiles', StudentProfilesView.as_view(), name='student_profiles'),
    path('student/profile/<str:student>', StudentProfileView.as_view(), name='student_profile'),
    path('student/activate', StudentActivationView.as_view(), name='activate'),
]