"""
This model maps many users to a single company, and defines their role.
"""
from user.models import User

from django.db import models
from djchoices import ChoiceItem, DjangoChoices

from ..models import Entity


class Member(models.Model):
    """
    A company has many members (users) with different permissions (roles).
    """
    # permission roles
    class Roles(DjangoChoices):
        MEMBER = ChoiceItem('member')
        EDITOR = ChoiceItem('editor')
        OWNER = ChoiceItem('owner')

    # fields
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member')
    role = models.CharField(max_length=30, choices=Roles.choices)

    class Meta:
        unique_together = ('entity', 'user')

    @staticmethod
    def is_editor(user: User, entity: Entity) -> bool:
        """
        An editor is an EDITOR or an OWNER.
        An editor can edit a company.
        :param user: the user to check
        :param company: the company the user belongs to
        :return: True if the user is administrator+ else False
        """
        try:
            member = Member.objects.filter(user=user, entity=entity)[0]
        except IndexError:
            return False

        if member.role in [Member.Roles.EDITOR, Member.Roles.OWNER]:
            return True
        return False

    @staticmethod
    def is_owner(user: User, entity: Entity) -> bool:
        try:
            member = Member.objects.filter(user=user, entity=entity)[0]
        except IndexError:
            return False

        if member.role == Member.Roles.OWNER:
            return True
        return False

    @staticmethod
    def get_members(entity: Entity) -> []:
        """
        :param role: Get members with the specific role
        :return: a list of Members (users)
        """

        members = Member.objects.filter(entity=entity).select_related('user')
        return members

