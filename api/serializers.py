from rest_framework import serializers
from api.models import User, Attendance, Course
from django.utils import timezone


class UserSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "phone_number", "courses", "occupation", "date_created", "date_updated"]
    def create(self, validated_data):
        request = self.context.get('request')
        id = validated_data["phone_number"]
        validated_data["id"] = id
        #creators_id = f'Attendance-ID_?code={validated_data["username"]}'
        #validated_data["creators_id"] = creators_id
        user = User.objects.create(**validated_data)
        return user

class CourseSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()

    class Meta:
        model = Course
        fields = ["id", "course_code","date_created", "date_updated"]
        
        
    def create(self, validated_data):
        highest_id = Course.objects.all().order_by('-id').first()
        new_id = highest_id.id + 1 if highest_id else 1
        course = Course.objects.create(id=new_id, **validated_data)
        
        return course
class AttendanceSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    #user = UserSerializers(read_only=True)
    course = CourseSerializers(read_only=True)
    course_id = serializers.CharField(max_length=100, write_only=True)
    #creators_id = serializers.CharField(max_length=10, write_only=True)
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()

    class Meta:
        model = Attendance
        fields = ["id", "attenders_id", "course_id", "course", "date_created", "date_updated"]
        
        
    def create(self, validated_data):
        course_id = validated_data["course_id"]
        attenders_id = validated_data["attenders_id"]
        
        # Get the course
        try:
            course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            raise serializers.ValidationError("Course does not exist")

        # Check if attendance already exists for this user and course today
        today = timezone.now().date()
        print(today)
        existing_attendance = Attendance.objects.filter(
            course=course,
            attenders_id=attenders_id,
            date_created=today
        ).first()

        if existing_attendance:
            raise serializers.ValidationError("Attendance already taken for this course today")

        # Create the attendance record
        attendance = Attendance.objects.create(course=course, **validated_data)
        return attendance

