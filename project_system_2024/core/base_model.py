from django.db import models


class OnlyActiveManager(models.Manager):
    def get_queryset(self):
        return (super(OnlyActiveManager, self).get_queryset()
                .filter(is_active=True))


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True,
                                      verbose_name='created at')
    updated_at = models.DateTimeField(auto_now=True,
                                      verbose_name='updated at')
    is_active = models.BooleanField(default=True)

    objects = models.Manager()
    active = OnlyActiveManager()

    class Meta:
        abstract = True
        default_manager_name = 'active'

    def delete(self):
        self.is_active = False
        self.save()
