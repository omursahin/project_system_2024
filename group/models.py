from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class Group(BaseModel):
    owner = models.ForeignKey('account.MyUser',
                              on_delete=models.CASCADE, related_name='group')
    semester_course = models.ForeignKey(
        'semester_course.SemesterCourse',
        on_delete=models.CASCADE, related_name='group')
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255, default='', blank=True)
    max_size = models.IntegerField()
    status = models.CharField(
        max_length=1, choices=(
            ('A', 'Approved'), ('D', 'Draft'), ('R', 'Rejected')),
        default='D')
    invitation_code = models.CharField(max_length=6)

    def __str__(self):
        return f"{self.title}"

    class Meta:
        db_table = 'group'
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        ordering = ['-created_at']
