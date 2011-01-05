from django.db import models

class Matchup(models.Model):
    round_name  = models.CharField(max_length=30)
    winner      = models.ForeignKey('players.player')
    win_slot    = models.OneToOneField('Slot',related_name='win_source')
    lose_slot   = models.OneToOneField('Slot',related_name='lose_source')

class Slot(models.Model):
    player  = models.ForeignKey('players.player')
    matchup     = models.ForeignKey(Matchup)

