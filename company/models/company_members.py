"""
This model maps many users to a single company, and defines their role.
"""
from user.models import User

from django.db import models
from djchoices import ChoiceItem, DjangoChoices

from ..models import Company


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
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='members')
    role = models.CharField(max_length=30, choices=Roles.choices)

    class Meta:
        unique_together = ('company', 'user')

    @classmethod
    def is_editor(cls, user: User, company: Company) -> bool:
        """
        An editor is an EDITOR or an OWNER.
        An editor can edit a company.
        :param user: the user to check
        :param company: the company the user belongs to
        :return: True if the user is administrator+ else False
        """
        member = cls.objects.filter(
            user=user,
            company=company
        )[0]

        if member.role in [cls.Roles.EDITOR, cls.Roles.OWNER]:
            return True
        return False

    @classmethod
    def get_members(cls, role: Roles) -> []:
        """
        :param role: Get members with the specific role
        :return: a list of Members (users)
        """
        member_ids = cls.objects.filter(
            role=role
        ).values_list('user', flat=True)
        return \
            User.objects.filter(id__in=member_ids)
