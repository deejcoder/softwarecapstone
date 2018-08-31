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
            company_name="Activision",
            company_size=5,
            industry="What?",
            specialist_area="IT",
            contact_phone="0800123123",
            contact_email="contact@act",
            website="activision",
            type_of_business="Security"
        )
        u = User.objects.create_user(
            username="activision",
            first_name="Dylan",
            last_name="Tonks"
        )
        CompanyMembers.objects.create(
            company=c,
            user=u,
            role=CompanyMembers.Roles.ADMIN
        )

    def test_fetch_owners(self):
        admins = CompanyMembers.get_administrators()
        company = Company.objects.get(company_name="Activision")
        print(admins)
        # there must be only one owner
        print(CompanyMembers.is_administrator(admins[0], company))
