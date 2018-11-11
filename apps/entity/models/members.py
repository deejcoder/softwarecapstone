"""
This model maps many users to a single company, and defines their role.
"""
from operator import itemgetter

from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from djchoices import ChoiceItem, DjangoChoices

from apps.user.models import User

from ..models import Entity


# permission roles
class Roles(DjangoChoices):
    OWNER = ChoiceItem('owner', order=1)
    EDITOR = ChoiceItem('editor', order=2)
    MEMBER = ChoiceItem('member', order=3)

    @classmethod
    def sort_roles(cls, member) -> int:
        choice = member.role
        return cls.get_choice(choice).order


class Member(models.Model):
    """
    A company has many members (users) with different permissions (roles).
    """

    # fields
    entity = models.ForeignKey(Entity, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='member')
    role = models.CharField(max_length=30, choices=Roles.choices)

    class Meta:
        unique_together = ('entity', 'user')

    def __str__(self):
        return "{0} ({1})".format(self.user.username, self.pk)

    @classmethod
    def sort_by_role(cls, member_list: []) -> []:
        """
        Accepts a list of members and sorts them by
        role
        """
        return sorted(member_list, key=Roles.sort_roles)

    @staticmethod
    def is_editor(user: User, entity: Entity) -> bool:
        """
        An editor is an EDITOR or an OWNER.
        An editor can edit a company.
        :param user: the user to check
        :param company: the company the user belongs to
        :return: True if the user is administrator+ else False
        """
        # user not logged in
        if not user.is_authenticated:
            return False

        try:
            member = Member.objects.filter(user=user, entity=entity)[0]
        except IndexError:
            return False

        if member.role in [Roles.EDITOR, Roles.OWNER]:
            return True
        return False

    @staticmethod
    def is_owner(user: User, entity: Entity) -> bool:
        # not a valid user
        if not user.is_authenticated:
            return False

        try:
            member = Member.objects.filter(user=user, entity=entity)[0]
        except IndexError:
            return False

        if member.role == Roles.OWNER:
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

    @staticmethod
    def is_editor_any(user: User) -> bool:

        # user is not logged in
        if not user.is_authenticated:
            return False

        try:
            Member.objects \
                .filter(user=user) \
                .filter(role=Roles.EDITOR)[0]
        except IndexError:
            return False
        return True

    @staticmethod
    def is_owner_any(user: User) -> bool:

        # user is not logged in
        if not user.is_authenticated:
            return False

        try:
            Member.objects \
                .filter(user=user) \
                .filter(role=Roles.OWNER)[0]
        except IndexError:
            return False
        return True

    @staticmethod
    def get_user_company(user: User):
        if not user.is_authenticated:
            return None

        entities = Member.objects \
            .filter(user=user) \
            .filter(role=Roles.EDITOR) \
            | Member.objects \
            .filter(user=user) \
            .filter(role=Roles.OWNER)
        
        for entity in entities:
            try:
                if entity.entity.company:
                    return entity.entity.company
            except ObjectDoesNotExist:
                pass
        return None


    @staticmethod
    def get_user_group(user: User):
        if not user.is_authenticated:
            return None

        entities = Member.objects \
            .filter(user=user) \
            .filter(role=Roles.EDITOR) \
            | Member.objects \
            .filter(user=user) \
            .filter(role=Roles.OWNER)
                   
        for entity in entities:
            try:
                if entity.entity.group:
                    return entity.entity.group
            except ObjectDoesNotExist:
                pass
        return None
