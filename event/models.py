from django.db import models
from entity.models import Entity


class Event(models.Model):

    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='event')
    title = models.CharField(max_length=80)
    date = models.DateField(default=None)
    time = models.TimeField(default=None)
    location = models.CharField(max_length=80)
    description = models.TextField(max_length=500*5.1)  # 5.1 = average word length

    def __str__(self):
        return "{0} ({1})".format(self.title, self.pk)
    
    def get_events(entity: Entity) -> []:
        """
        Returns a list of events associated with a particular entity (group or company)
        """
        events = Event.objects.filter(entity=entity).select_related('entity')
        return events
    
