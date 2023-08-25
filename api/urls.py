from django.urls import path
from .views import (CreateAttendance, CreateUser, GetAllAttendance, 
                    GetAllUsers, GetAttendance, GetUser, UpdateAttendance, 
                    UpdateUser, DeleteUser, DeleteAttendance)

# app_name = 'api'

urlpatterns = [
    path("create_user", CreateUser.as_view(), name="create-user"),
    path("users", GetAllUsers.as_view(), name="users"),
    path("user/get/<str:phone_number>", GetUser.as_view(), name="user"),
    path("user/update/<str:pk>", UpdateUser.as_view(), name="update-user"),
    path("user/delete/<str:pk>", DeleteUser.as_view(), name="delete-user"),
    #attendance
    path("create_attendance", CreateAttendance.as_view(), name="create-user"),
    path("attendances", GetAllAttendance.as_view(), name="attendances"),
    path("attendance/get/<str:pk>", GetAttendance.as_view(), name="attendance"),
    path("attendance/update/<str:pk>", UpdateAttendance.as_view(), name="update-attendance"),
    path("attendance/delete/<str:pk>", DeleteAttendance.as_view(), name="delete-attendance"),
]