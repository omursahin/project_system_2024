from django.db import models

from project_system_2024.core.base_model import BaseModel


# Create your models here.
class GroupMember(BaseModel):
    group = models.ForeignKey('group.Group',
                              on_delete=models.CASCADE,
                              related_name='group_member')
    member = models.ForeignKey(
        'account.MyUser',
        on_delete=models.CASCADE, related_name='group_member')
    is_accepted = models.BooleanField(default=False)
    is_supervisor = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.group}-{self.member}"

    class Meta:
        db_table = 'group_member'
        verbose_name = 'Group Member'
        verbose_name_plural = 'Group Members'
        ordering = ['-created_at']
