from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class ProjectReport(BaseModel):
    project = models.ForeignKey('group_project.GroupProject', on_delete=models.CASCADE )
    report = models.ForeignKey('report.Report', on_delete=models.CASCADE )
    file = models.FileField(upload_to='data', null=True, blank=True)
    description = models.CharField(max_length=255, null=True, blank=True)
    is_submitted = models.BooleanField(default=False)
    version = models.IntegerField(null=True, blank=True)
    plagiarism_file = models.FileField(upload_to= 'data', null=True, blank=True)
    plagiarism_rate = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.id}"

    class Meta:
        db_table = 'project_report'
        verbose_name = 'Project Report'
        verbose_name_plural = 'Project Reports'
        ordering = ['-created_at']
