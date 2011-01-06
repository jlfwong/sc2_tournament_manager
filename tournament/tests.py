from django.test import TestCase
from tournament.models import Matchup, Slot
from django.test.client import Client
from django.contrib.auth.models import User

class MatchupAdminTest(TestCase):
    def setUp(self): 
        """ Create a superuser and log in """
        user = User.objects.create_user('test_user','test@test.com','password')
        user.is_superuser = True
        user.is_staff = True
        user.save()

        self.client = Client()
        self.assertTrue(self.client.login(
            username='test_user',
            password='password',
        ))


    def test_get_add(self):
        resp = self.client.get('/admin/tournament/matchup/add/')
        self.assertEqual(resp.status_code,200)
        self.assertContains(resp,'Add matchup')
