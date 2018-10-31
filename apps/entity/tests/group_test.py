"""
Tests the Company & CompanyMembers models
"""
import datetime
from apps.user.models import User

from django.test import TestCase

from apps.entity.models import Member, Application
from apps.entity.models.group import Group


class GroupModelTestCase(TestCase):
    """
    Results: must resize some fields max_length,
    and set some fields to required.
    Must also split the 'address' field into:
        * Street address
        * Suburb
    """
    def setUp(self):

        g = Group.objects.create(
            name="PUGB",
            website="pugb@palmy.co.nz",
            description="Something special!"
        )
        u1 = User.objects.create_user(
            username="linuxnerd",
            first_name="Dylan",
            last_name="Tonks"
        )
        u2 = User.objects.create_user(
            username="pugbco",
            first_name="Master",
            last_name="Chief"
        )
        Member.objects.create(
            entity=g,
            user=u1,
            role=Member.Roles.EDITOR
        )
        Member.objects.create(
            entity=g,
            user=u2,
            role=Member.Roles.OWNER
        )

    def test_editors(self):
        # get group & its members
        group = Group.objects.get(name="PUGB")
        editors = Member.get_members(group)

        # there are two editors (1 owner, 1 editor)
        self.assertTrue(len(editors) == 2)
        # the users are editors
        self.assertTrue(Member.is_editor(editors[0].user, group))
        self.assertTrue(Member.is_editor(editors[1].user, group))

        # test company applications
        self.assertEqual(
            group.application.date_submitted,
            datetime.date.today()
        )

        group.application.approve(
            user=editors[0].user,
            comment="A well made application, approved!"
        )
        self.assertEqual(
            group.application.status,
            Application.StatusType.Approved
        )

        print("""
            Group test successful. A single group was created,
            group.name=%s
            total group editors: %d
            editor #1: %s
            editor #2: %s
            A group application was also created with this group,
            group.application.date_submitted=%s
            group.application.date_approved=%s
            group.application.approved_by=%s
            group.application.comment=%s
            """ % (
                group.name, len(editors), editors[0], editors[1],
                group.application.date_submitted, group.application.date_approved, group.application.approved_by,
                group.application.comment
            )
        )