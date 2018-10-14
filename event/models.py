from django.db import models
from entity.models import Entity


class Event(models.Model):

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='event')
    title = models.CharField(max_length=80)
    time = models.DateTimeField()
    location = models.CharField(max_length=80)
    description = models.TextField(max_length=500*5.1)  # 5.1 = average word length

    class Meta:
        ordering = ('-time')


