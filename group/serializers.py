import uuid

from rest_framework import serializers

from group.models import Group
from semester_course.models import SemesterCourse
from semester_course_student.models import SemesterCourseStudent


class ValidationError:
    pass




class GroupSerializer(serializers.ModelSerializer):
    owner = serializers.HiddenField(default=serializers.CurrentUserDefault())
    max_size = serializers.ReadOnlyField()
    invitation_code = serializers.ReadOnlyField()

    class Meta:
        model = Group
        fields = '__all__'

    def create(self, validated_data):
         semester_course = (SemesterCourse.active
                        .get(id=validated_data['semester_course'].id))
         validated_data['max_size'] = semester_course.max_grup_size
         validated_data['invitation_code'] = str(uuid.uuid4())[:6].upper()

         return Group.objects.create(**validated_data)

    def validate(self, attrs):
        request = self.context['request']
        user = request.user
        semester_course = attrs['semester_course']

        if user.is_superuser == False:
            #ogrenci semester_course a kayıtlı mı kontrol et
            existing_student = SemesterCourseStudent.objects.filter(semester_course=semester_course, student=user)
            if not existing_student.exists():
                raise serializers.ValidationError("Öğrenci o dönemin kursuna kayıtlı değil ise grup oluşturamaz.")

            #ogrencinin zaten bir grup oluşturup oluşturmadığını kontrol et
            existing_groups = Group.objects.filter(owner=user, semester_course=semester_course)
            if self.instance:  # Güncelleme işlemi
                existing_groups = existing_groups.exclude(id=self.instance.id)
            if existing_groups.exists():
                raise serializers.ValidationError("Bir öğrenci birden fazla grup oluşturamaz.")

            # SemesterCourse'un maksimum grup sayısını kontrol et
            if Group.objects.filter(semester_course=semester_course).count() >= semester_course.max_grup_size:
                raise serializers.ValidationError(
                    f"Bu ders döneminde en fazla {semester_course.max_grup_size} grup oluşturulabilir.")
        return attrs