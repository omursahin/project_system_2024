import uuid

from rest_framework import serializers

from group.models import Group
from semester_course.models import SemesterCourse


class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Group
        fields = '__all__'

    def create(self, validated_data):
        semester_course = (SemesterCourse.active
                           .get(id=validated_data['semester_course'].id))
        validated_data['max_size'] = semester_course.max_grup_size
        validated_data['invitation_code'] = str(uuid.uuid4())[:6].upper()

        return Group.objects.create(**validated_data)
