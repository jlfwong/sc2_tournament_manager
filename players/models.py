from django.db import models

LEAGUE_CHOICES = (
    ('b', 'Bronze'),
    ('s', 'Silver'),
    ('g', 'Gold'),
    ('p', 'Platinum'),
    ('d', 'Diamond')
)

RACE_CHOICES = (
    ('t', 'Terran'),
    ('p', 'Protoss'),
    ('z', 'Zerg'),
    ('r', 'Random')
)

class Player(models.Model):
    name        = models.CharField(max_length=30)
    league      = models.CharField(max_length=1, choices=LEAGUE_CHOICES)
    race        = models.CharField(max_length=1, choices=RACE_CHOICES)
    charcode    = models.IntegerField()
    bnet_id     = models.IntegerField()

    class Admin: pass

