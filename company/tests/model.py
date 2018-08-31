"""
Tests the Company & CompanyMembers models
"""
from user.models import User

from django.test import TestCase

from ..models import Company, CompanyMembers


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
        CompanyMembers.objects.create(
            company=c,
            user=u1,
            role=CompanyMembers.Roles.EDITOR
        )
        CompanyMembers.objects.create(
            company=c,
            user=u2,
            role=CompanyMembers.Roles.OWNER
        )

    def test_editors(self):
        # get editors & owners
        editors = CompanyMembers.get_members(CompanyMembers.Roles.EDITOR) | \
            CompanyMembers.get_members(CompanyMembers.Roles.OWNER)
        company = Company.objects.get(name="Activision")

        # there are two editors (1 owner, 1 editor)
        self.assertTrue(len(editors) == 2)
        # the users are editors
        self.assertTrue(CompanyMembers.is_editor(editors[0], company))
        self.assertTrue(CompanyMembers.is_editor(editors[1], company))

