from rest_framework import serializers
from .models import CustomUser, StudentProfile
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed, NotFound, ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError


class UserActivationSerializer(serializers.Serializer):
    id = serializers.CharField()
    email = serializers.EmailField()
    is_active = serializers.BooleanField()


class StudentRegisterSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    class Meta:
        model= CustomUser
        fields=['id', 'email', 'full_name', 'phone_no', 'role', 'is_active', 'password', 'date_created', 'date_updated']
    
    def validate(self, attrs):
        role = attrs.get('role', '')
        if str(role).lower() == 'student':
            return attrs
        else:
            raise ValidationError("User role should be set to 'Student'")

    def create(self, validated_data):
        user = CustomUser.objects.create_student(**validated_data)
        return user
    
class StudentLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)
    def get_tokens(self, obj):
        user = CustomUser.objects.get(email=obj['email'])
        return user.tokens()

    class Meta:
        model = CustomUser
        fields = ['email', 'password', 'tokens']


    def validate(self, attrs):
        email = attrs.get('email', '')
        #matric_no = attrs.get('matric_no', '')
        password = attrs.get('password', '')
 
        user = CustomUser.objects.get(email=email)
        if not user.is_active:
            raise AuthenticationFailed("User Not Active") 

        user = auth.authenticate(email=email, password=password)

        if not user:
            raise AuthenticationFailed("Credentials Not Valid, Try Again")
        
        if str(user.role).lower() != 'student':
            raise AuthenticationFailed("User role should be set to 'Student'")
        
        return {
            "email":user.email,
            "tokens":user.tokens()
        }
    
class StudentLogoutSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()
    def validate(self, attrs):
        self.token = attrs['refresh_token']
        return attrs
    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            self.fail('bad_token')


### STUDENT PROFILE SERIALIZER

class StudentProfileSerializer(serializers.ModelSerializer):
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()

    class Meta:
        model = StudentProfile
        fields = ['student', 'matric_no', 'faculty', 'department', 'level', 'date_created', 'date_updated']

    def validate(self, attrs):
        student = attrs['student']
        if CustomUser.objects.filter(email=student.email).exists() and str(student.role).lower()=='student':
            return attrs
        else:
            raise ValidationError("Student not found")