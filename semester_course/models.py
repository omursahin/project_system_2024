from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class SemesterCourse(BaseModel):
    semester = models.ForeignKey('semester.Semester', on_delete=models.CASCADE,
                                 related_name="semester_courses")
    course = models.ForeignKey('course.Course',
                               on_delete=models.CASCADE,
                               related_name="semester_courses")

    max_grup_size = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.semester}-{self.course}"

    class Meta:
        db_table = 'semester_course'
        verbose_name = 'Semester Course'
        verbose_name_plural = 'Semester Courses'
        ordering = ['-created_at']
        # unique_together = ('semester', 'course')
