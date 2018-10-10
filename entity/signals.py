"""
This file defines signals. Signals are triggers, and are triggered when
something happens, such as when an object saves.
"""

from django.db.models.signals import post_save
from django.dispatch import receiver

from entity.models import Application
from entity.models.company import Company
# from entity.models.groups import Group


@receiver(post_save, sender=Company)
def create_company_application(sender, instance, created, **kwargs):
    """
    Creates a new company application whenever a company is created.
    """
    if created: 
        Application.objects.create(entity=instance)

"""
@receiver(post_save, sender=Group)
def create_group_application(sender, instance, created, **kwargs):
    # Creates a new group application when a group is created.
    if created: 
        Application.objects.create(entity=instance)
"""
