"""
This model adds functionality for company applications.
An application references a company.
It should be noted, a company's application status is stored in the Company
model.
"""

import datetime
from user.models import User
from ..models import Company

from django.db import models
from djchoices import ChoiceItem, DjangoChoices


class CompanyApplication(models.Model):

    class StatusType(DjangoChoices):
        Pending = ChoiceItem('pending')
        Approved = ChoiceItem('approved')
        Denied = ChoiceItem('denied')

    company = models.OneToOneField(
        Company,
        on_delete=models.CASCADE,
        related_name='application',
    )
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    date_approved = models.DateField(null=True, default=None)
    date_submitted = models.DateField(default=datetime.date.today())
    comment = models.TextField(max_length=300, null=True, default=None)
    status = models.CharField(
        max_length=20,
        choices=StatusType.choices,
        default=StatusType.Pending
    )

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
