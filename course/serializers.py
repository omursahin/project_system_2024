from rest_framework import serializers

from course.models import Course


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'

    def create(self, validated_data):
        try:
            course = Course.objects.create(**validated_data)
            return course
        except Exception as e:
            raise serializers.ValidationError(e)
