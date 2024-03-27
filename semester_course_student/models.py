from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class SemesterCourseStudent(BaseModel):
    semester_course = models.ForeignKey('semester_course.SemesterCourse', on_delete=models.CASCADE,
                                        related_name="semester_course_students")

    student = models.ForeignKey('account.MyUser', on_delete=models.CASCADE,
                                related_name="semester_course_students")

    mid_term = models.IntegerField(null=True, blank=True)
    final = models.IntegerField(null=True, blank=True)
    make_up = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.semester_course}-{self.student}"

    class Meta:
        db_table = 'semester_course_student'
        verbose_name = 'Semester Course Student'
        verbose_name_plural = 'Semester Course Students'
        ordering = ['-created_at']
