from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class Semester(BaseModel):
    term = models.CharField(max_length=20, blank=False, null=False)
    year = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.term}-{self.year}"

    class Meta:
        db_table = 'semester'
        verbose_name = 'Semester'
        verbose_name_plural = 'Semesters'
        ordering = ['-created_at']
