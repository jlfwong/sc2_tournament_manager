from django.test import TestCase
from tournament.models import Matchup
from players.models import Player
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

    def test_get_list(self):
        resp = self.client.get('/admin/tournament/matchup/')
        self.assertEqual(resp.status_code,200)
        self.assertContains(resp,'Select matchup to change')


class MatchupTest(TestCase):
    fixtures = ['players.json']

    def test_method_participants(self):
        alice   = Player.objects.get(name='alice')
        bob     = Player.objects.get(name='bob')

        matchup = Matchup(name='Test Matchup',player_1=alice,player_2=bob)
        matchup.save()

        self.assertTrue(alice in matchup.participants())
        self.assertTrue(bob in matchup.participants())

    def test_attr_loser(self):
        alice   = Player.objects.get(name='alice')
        bob     = Player.objects.get(name='bob')

        matchup = Matchup(name='Test Matchup',player_1=alice,player_2=bob,winner=alice)
        matchup.save()

        self.assertEqual(matchup.winner,alice)
        self.assertEqual(matchup.loser,bob)
        

    def test_winner_propogation(self):
        alice   = Player.objects.get(name='alice')
        bob     = Player.objects.get(name='bob')
        candice = Player.objects.get(name='candice')
        david   = Player.objects.get(name='david')

        Matchup(name='Finals').save()

        Matchup(name='Semi East',
                player_1=alice,
                player_2=bob,
                winner_matchup=Matchup.objects.get(name='Finals')).save()

        Matchup(name='Semi West',
                player_1=candice,
                player_2=david,
                winner_matchup=Matchup.objects.get(name='Finals')).save()
        
        # Bob wins Semi East
        semi_east = Matchup.objects.get(name='Semi East')
        semi_east.winner = bob
        semi_east.save()

        # Candice wins Semi West
        semi_west = Matchup.objects.get(name='Semi West')
        semi_west.winner = candice
        semi_west.save()

        finals = Matchup.objects.get(name='Finals')
        self.assertTrue(bob in finals.participants())
        self.assertTrue(candice in finals.participants())

        # Correction: Alice wins Semi East
        semi_east = Matchup.objects.get(name='Semi East')
        semi_east.winner = alice
        semi_east.save()

        finals = Matchup.objects.get(name='Finals')
        self.assertTrue(alice in finals.participants())
        self.assertTrue(bob not in finals.participants())
        self.assertTrue(candice in finals.participants())

        # Correction: David wins Semi West
        semi_west = Matchup.objects.get(name='Semi West')
        semi_west.winner = david
        semi_west.save()

        finals = Matchup.objects.get(name='Finals')
        self.assertTrue(david in finals.participants())
        self.assertTrue(candice not in finals.participants())
        self.assertTrue(alice in finals.participants())
