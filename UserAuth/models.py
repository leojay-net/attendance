from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from .managers import CustomUserManager
from .utils import generate_id
from django.utils.translation import gettext_lazy as _


class CustomUser(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(default=generate_id,primary_key=True, max_length=100, blank=False, null=False)
    full_name = models.CharField(max_length= 300, blank=False, null=False)
    email = models.EmailField(_("email address"), unique=True, db_index=True, blank=False, null=False)
    phone_no = models.CharField(max_length=15, blank=False, null=False)
    role = models.CharField(max_length=30, blank=False, null=False)
    is_active = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    updated_date = models.DateTimeField('date_created' ,auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        return self.email
    
    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return{
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }

class StudentProfile(models.Model):
    student = models.OneToOneField(CustomUser, on_delete=models.CASCADE, primary_key=True)
    matric_no = models.CharField(max_length=100, blank=False, null=False)
    faculty = models.CharField(max_length=300, blank=False, null=False)
    department = models.CharField(max_length=300, blank=False, null=False)
    level = models.IntegerField()
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField('date_created' ,auto_now=True)

    def __str__(self) -> str:
        return str(self.student.email)
