from rest_framework import serializers

from academician_group_grade.models import AcademicianGroupGrade


class AcademicianGroupGradeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicianGroupGrade
        fields = '__all__'
