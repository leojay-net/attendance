from rest_framework import serializers
from api.models import User, Attendance


class UserSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()
    creators_id = serializers.ReadOnlyField()

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "username", "email", "creators_id", "occupation", "date_created", "date_updated"]
    def create(self, validated_data):
        request = self.context.get('request')
        creators_id = f'Attendance-ID_?code={validated_data["username"]}'
        validated_data["creators_id"] = creators_id
        user = User.objects.create(**validated_data)
        return user
    
class AttendanceSerializers(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    user = UserSerializers(read_only=True)
    # creators_id = serializers.ReadOnlyField()
    date_created = serializers.ReadOnlyField()
    date_updated = serializers.ReadOnlyField()

    class Meta:
        model = Attendance
        fields = ["id", "full_name", "title", "subject", "attenders_id", "user", "creators_id", "date_created", "date_updated"]
        
        
    def create(self, validated_data):
        request = self.context.get('request')
        username = validated_data["creators_id"].replace("Attendance-ID_?code=", "")
        print(username)
        user = User.objects.get(username=username)
        # validated_data["user"] = user
        attendance = Attendance.objects.create(user=user, **validated_data)
        return attendance