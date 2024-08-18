from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from .serializers import (StudentRegisterSerializer, StudentLogoutSerializer, StudentLoginSerializer,
                          StudentProfileSerializer, UserActivationSerializer)
from .models import StudentProfile, CustomUser
from rest_framework import status, permissions
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .email_validation import send_confirmation_mail, activate_user
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_decode


class StudentRegisterView(GenericAPIView):
    serializer_class = StudentRegisterSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        print("user", user.phone_no)
        # user = CustomUser.objects.get(id=serializer.data['id'])
        con_email = send_confirmation_mail(user=user)
        print("cpn_email:",con_email)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

class StudentActivationView(GenericAPIView):
    serializer_class = UserActivationSerializer

    def get(self, request):
        # uidb64 = request.query_params.get('uid')
        # token = request.query_params.get('token')
        uid = request.GET.get('uid')
        token = request.GET.get('token')
        try:
            uid = force_text(urlsafe_base64_decode(uid))
            user = CustomUser.objects.get(id=uid)
        except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
        activate = activate_user(user, token)
        if activate:
            return Response({
                'id':user.id,
                'email':user.email,
                'is_active':user.is_active,
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'response':"Validation Link Invalid"
            }, status=status.HTTP_406_NOT_ACCEPTABLE)

class StudentLoginView(GenericAPIView):
    serializer_class = StudentLoginSerializer

    def post(self, request):
        user = request.data
        serializer = self.serializer_class(data = user)
        serializer.is_valid(raise_exception=True)
        # serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    
class StudentLogoutView(GenericAPIView):
    serializer_class = StudentLogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

class StudentProfileCreateView(GenericAPIView):
    serializer_class = StudentProfileSerializer

    def post(self, request):
        profile = request.data
        serializer = self.serializer_class(data=profile)
        serializer.is_valid()
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
class StudentProfilesView(ListAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    queryset = StudentProfile.objects.all()
    filterset_fields = ['student', 'matric_no', 'faculty', 'department', 'level']

class StudentProfileView(RetrieveAPIView):
    serializer_class = StudentProfileSerializer
    permission_classes = [permissions.IsAuthenticated]
    queryset = StudentProfile.objects.all()
    lookup_field = "student"
