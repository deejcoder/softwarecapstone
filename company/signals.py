"""
All signals. Signals are triggers and are triggered when something happens
such as when a model saves. Refer to Django signals.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Company, CompanyApplication


@receiver(post_save, sender=Company)
def create_company_application(sender, instance, created, **kwargs):
    """
    Creates a new company application whenever a new company is created.
    """
    if created and instance.status == Company.StatusType.Pending:
        CompanyApplication.objects.create(
            company=instance,
        )
