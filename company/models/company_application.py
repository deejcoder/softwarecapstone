"""
This model adds functionality for company applications.
An application references a company.
It should be noted, a company's application status is stored in the Company
model.
"""

import datetime
from user.models import User

from django.db import models

from ..models import Company


class CompanyApplication(models.Model):

    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    approved_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, default=None)
    date_approved = models.DateField(null=True, default=None)
    date_submitted = models.DateField(default=datetime.date.today)
    comment = models.TextField(max_length=300, null=True, default=None)

    def approve(self, user: User, comment: str) -> bool:
        """
        Approves a company's application
        """
        if self.company.status != Company.StatusType.Approved:
            self.company.status = Company.StatusType.Approved
            self.approved_by = user
            self.date_approved = datetime.date.today
            self.comment = comment
            return True

        else:
            return False
