from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class GroupProject(BaseModel):
    group_project = (models.
                     ForeignKey('group.Group',
                                on_delete=models.CASCADE,
                                related_name="group_project"))

    title = models.CharField(max_length=255, blank=False, null=False)
    description = models.CharField(max_length=255, blank=True, null=True)
    is_approved = models.BooleanField()
    STATUS_CHOICES = (("A", "Approved"),
                      ("P", "Pending"),
                      ("D", "Draft"),
                      ("R", "Rejected"))

    status = models.CharField(max_length=255, blank=False, null=False,
                              choices=STATUS_CHOICES)

    def __str__(self):
        return f"{self.group_project}"

    class Meta:
        db_table = 'group_project'
        verbose_name = 'Group Project'
        verbose_name_plural = 'Group Projects'
        ordering = ['-created_at']
