from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class Course(BaseModel):
    code = models.CharField(unique=True, max_length=20,
                            blank=False, null=False)
    title = models.CharField(max_length=32, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return f"{self.code}-{self.title}"

    class Meta:
        db_table = 'course'
        verbose_name = 'Course'
        verbose_name_plural = 'Courses'
        ordering = ['-created_at']
