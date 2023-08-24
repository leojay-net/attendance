from django.db import models
import uuid
from django.utils import timezone
# Create your models here.
class User(models.Model):
    id = models.CharField(max_length=64, default=str(uuid.uuid4()).replace("-", ""), unique=True, primary_key=True)
    username = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100, unique=True)
    occupation = models.CharField(max_length=50)
    creators_id = models.CharField(max_length=100)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField('date_created', auto_now=True)

    def __str__(self):
        return str(self.username)
    
    class Meta:
        ordering = ["-date_updated"]

class Attendance(models.Model):
    id = models.CharField(max_length=64, default=str(uuid.uuid4()).replace("-", ""), unique=True, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    creators_id = models.CharField(max_length=100)
    full_name = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    subject = models.CharField(max_length=100)
    attenders_id = models.CharField(max_length=100)
    date_created = models.DateField(default=timezone.now)
    date_updated = models.DateField('date_created', auto_now=True)



    def __str__(self):
        return str(self.user.username)
    
    class Meta:
        ordering = ["-date_updated"]




