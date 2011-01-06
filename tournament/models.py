from django.db import models
from django.db.models.signals import post_save

class Matchup(models.Model):
    name        = models.CharField(max_length=30)
    winner      = models.ForeignKey('players.player',blank=True,null=True)

    win_slot    = models.OneToOneField('Slot',  related_name='win_source', 
                                                blank=True,
                                                unique=True,
                                                null=True,
                                                verbose_name='Winner goes to',
                                                help_text='Leave blank for Finals')

    lose_slot   = models.OneToOneField('Slot',  related_name='lose_source',
                                                blank=True,
                                                unique=True,
                                                null=True,
                                                verbose_name='Loser goes to',
                                                help_text='Leave blank if loser is eliminated')
    
    def __str__(self):
        slots = self.slot_set.all()
        if len(slots) > 1 and slots[0].player:
            player_1_name = slots[0].player.name
        else:
            player_1_name = '???'

        if len(slots) > 2 and slots[0].player:
            player_2_name = slots[1].player.name
        else:
            player_2_name = '???'

        return "%s: %s vs. %s" % (self.name,player_1_name,player_2_name)

class Slot(models.Model):
    player  = models.ForeignKey('players.player',blank=True,null=True,help_text='Only set for the preliminary matches')
    matchup = models.ForeignKey(Matchup)

    def __str__(self):
        if type(self.id) == type(None):
            return "New Slot" 
        else:
            return "(Matchup: %s) id #%d" % (self.matchup.name, self.id)
