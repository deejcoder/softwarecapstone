"""
This file tests the user app, at the moment it focuses upon testing
the searching of consultants and users as well as their models.
"""

from django.test import TestCase

from ..models import Consultant, User


class ConsultantTestCase(TestCase):
    def setUp(self):

        # create some data...

        User.objects.create_user(
            username="dy1zan",
            first_name="Dylan",
            last_name="Jacob"
        )
        user = User.objects.create_user(
            username="erei",
            first_name="Dylan",
            last_name="Tonks"    
        )
        User.objects.create_user("octet")
        User.objects.create_user("dylan")
        User.objects.create_user("dy1an")

        # link new consultant to user: erei
        Consultant.objects.create(
            user=user,
            current_occupation="something special",
            services_offered="""
                We offer great computer repairs, advice and our
                Linux experts can help you with any Linux problems
                whatsoever!
            """
        )

    # test search methods for consultants
    def test_consultant_search(self):
        print("test_consultant_search...")
        for consultant in Consultant.search_consultants('computer'):
            print(consultant.user.username)

    # test search methods for users
    def test_user_search(self):
        print("test_user_search...")
        for user in User.search_users('dylan'):
            print(user.get_full_name())
