from django.db import models

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
        return self.name

class Slot(models.Model):
    player  = models.ForeignKey('players.player',blank=True,null=True,help_text='Only set for the preliminary matches')
    matchup = models.ForeignKey(Matchup)

    def __str__(self):
        if type(self.id) == type(None):
            return "New Slot" 
        else:
            return "(Matchup: %s) id #%d" % (self.matchup, self.id)
