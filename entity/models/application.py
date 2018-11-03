"""
This model adds functionality for company applications.
An application references a company.
It should be noted, a company's application status is stored in the Company
model.
"""

import datetime
from user.models import User

from django.db import models
from django.utils import timezone
from djchoices import ChoiceItem, DjangoChoices

from entity.models import Entity


class Application(models.Model):

    class StatusType(DjangoChoices):
        Pending = ChoiceItem('pending')
        Approved = ChoiceItem('approved')
        Denied = ChoiceItem('denied')

    entity = models.OneToOneField(Entity, on_delete=models.CASCADE, related_name='application')
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    date_approved = models.DateField(null=True, default=None)
    date_submitted = models.DateField(default=timezone.now)
    comment = models.TextField(max_length=300, null=True, default=None)
    status = models.CharField(max_length=20, choices=StatusType.choices, default=StatusType.Pending)

    def __str__(self):
        return "Application: {0} ({1})".format(self.entity.name, self.pk)

    def approve(self, user: User, comment: str) -> bool:
        """
        Approves a company's application
        """
        if self.status != self.StatusType.Approved:
            self.status = self.StatusType.Approved
            self.approved_by = user
            self.date_approved = datetime.date.today()
            self.comment = comment
            return True

        else:
            return False
