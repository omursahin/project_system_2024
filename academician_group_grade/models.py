from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class AcademicianGroupGrade(BaseModel):
    academician = (models.ForeignKey('account.MyUser',
                                     on_delete=models.CASCADE,
                                     related_name="academician_group_grade"))

    group = models.ForeignKey('group.Group', on_delete=models.CASCADE,
                              related_name="academician_group_grade")

    mid_term = models.IntegerField(blank=0)
    final = models.IntegerField(null=True, blank=True)
    make_up = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.academician}-{self.group}"

    class Meta:
        db_table = 'academician_group_grade'
        verbose_name = 'Academician Group Grade'
        verbose_name_plural = 'Academician Group Grades'
        ordering = ['-created_at']
