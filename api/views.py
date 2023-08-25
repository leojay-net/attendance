from django.shortcuts import render
from rest_framework.generics import (CreateAPIView, ListAPIView, RetrieveAPIView,
                                        UpdateAPIView, DestroyAPIView, GenericAPIView)
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django_filters.rest_framework import DjangoFilterBackend
from .serializers import UserSerializers, AttendanceSerializers
from .models import User, Attendance

# Create your views here.
class CreateUser(CreateAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()

    def post(self, request, format=None):
        # request.POST._mutable = True
        # request.data["creators_id"] = f'Attendance-ID_?code={request.data["username"]}'
        #print(request.data["creators_id"])
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"msg": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
class GetAllUsers(ListAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["occupation"]

class GetUser(RetrieveAPIView):
    serializer_class = UserSerializers
    queryset = User.objects.all()


class UpdateUser(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})
        

class DeleteUser(GenericAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                    "info": "Object_Project deleted"
                }
            )
        except Exception as e:
            return Response({"info": e.args})
        


### ATTENDANCE ENDPOINTS ###

class CreateAttendance(CreateAPIView):
    serializer_class = AttendanceSerializers
    queryset = Attendance.objects.all()

    def post(self, request, format=None):
        # username = str(request.data["creators_id"]).replace("Attendance-ID_?code=", "")
        # print(username)
        # user = User.objects.get(username=username)
        # request.data["user"] = user
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            print("saved")
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data={"msg": serializer.errors}, status=status.HTTP_406_NOT_ACCEPTABLE)
        
class GetAllAttendance(ListAPIView):
    serializer_class = AttendanceSerializers
    def get_queryset(self):
        querys = Attendance.objects.all()
        if self.request.GET.get('username') == None and self.request.GET.get('subject') == None:
            return querys
        elif self.request.GET.get('username') != None and self.request.GET.get('subject') != None:
            username = self.request.GET.get('username')
            subject = self.request.GET.get('subject')
            user  = User.objects.get(username=username)
            querys = querys.filter(user=user, subject=subject)
            return querys
        elif self.request.GET.get('username') != None and self.request.GET.get('subject') == None:
            username = self.request.GET.get('username')
            user  = User.objects.get(username=username)
            querys = querys.filter(user=user)
            return querys
        elif self.request.GET.get('username') == None and self.request.GET.get('subject') != None:
            subject = self.request.GET.get('subject')
            querys = querys.filter(subject=subject)
            return querys
        else:
            return []


        


class GetAttendance(RetrieveAPIView):
    serializer_class = AttendanceSerializers
    queryset = Attendance.objects.all()


class UpdateAttendance(UpdateAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializers

    def patch(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        else:
            return Response({"message": "failed", "details": serializer.errors})
        

class DeleteAttendance(GenericAPIView):
    queryset = Attendance.objects.all()
    serializer_class = AttendanceSerializers
    def delete(self, request, *args, **kwargs):
        try:
            instance = self.get_object()
            instance.delete()
            return Response({
                    "info": "Object_Project deleted"
                }
            )
        except Exception as e:
            return Response({"info": e.args})