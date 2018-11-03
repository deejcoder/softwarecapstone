"""
Tests the Company & CompanyMembers models
"""
import datetime
from apps.user.models import User

from django.test import TestCase

from apps.entity.models import Member, Application
from apps.entity.models.company import Company


class CompanyModelTestCase(TestCase):
    """
    Results: must resize some fields max_length,
    and set some fields to required.
    Must also split the 'address' field into:
        * Street address
        * Suburb
    """
    def setUp(self):

        c = Company.objects.create(
            name="Activision",
            size=5,
            industry="What?",
            specialist_area="IT",
            contact_phone="0800123123",
            contact_email="contact@act",
            website="activision",
            type_of_business="Security"
        )
        u1 = User.objects.create_user(
            username="activision",
            first_name="Dylan",
            last_name="Tonks"
        )
        u2 = User.objects.create_user(
            username="bungie",
            first_name="Master",
            last_name="Chief"
        )
        Member.objects.create(
            entity=c,
            user=u1,
            role=Member.Roles.EDITOR
        )
        Member.objects.create(
            entity=c,
            user=u2,
            role=Member.Roles.OWNER
        )

    def test_editors(self):
        # get editors & owners
        company = Company.objects.get(name="Activision")
        editors = Member.get_members(company)

        # there are two editors (1 owner, 1 editor)
        self.assertTrue(len(editors) == 2)
        # the users are editors
        self.assertTrue(Member.is_editor(editors[0].user, company))
        self.assertTrue(Member.is_editor(editors[1].user, company))

        # test company applications
        self.assertEqual(
            company.application.date_submitted,
            datetime.date.today()
        )

        company.application.approve(
            user=editors[0].user,
            comment="A well made application, approved!"
        )
        self.assertEqual(
            company.application.status,
            Application.StatusType.Approved
        )

        print("""
            Company test successful. A single company was created,
            company.name=%s
            company.size=%d
            total company editors: %d
            editor #1: %s
            editor #2: %s
            A company application was also created with this company,
            company.application.date_submitted=%s
            company.application.date_approved=%s
            company.application.approved_by=%s
            company.application.comment=%s
            """ % (
                company.name, company.size, len(editors), editors[0], editors[1],
                company.application.date_submitted, company.application.date_approved, company.application.approved_by,
                company.application.comment
            )
        )