from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class Report(BaseModel):
    semester_course = models.ForeignKey('semester_course.SemesterCourse',
                                        on_delete=models.CASCADE,
                                        related_name="reports")
    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, default='')
    is_public = models.BooleanField(default=False, blank=False, null=False)
    is_final = models.BooleanField(default=False, blank=False, null=False)

    def __str__(self):
        return f"{self.semester_course}-{self.title}"

    class Meta:
        db_table = 'report'
        verbose_name = 'Report'
        verbose_name_plural = 'Reports'
        ordering = ['-created_at']
