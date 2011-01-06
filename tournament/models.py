from django.db import models

class Matchup(models.Model):
    name        = models.CharField(max_length=30)
    winner      = models.ForeignKey('players.player',blank=True,null=True)

    winner_matchup  = models.OneToOneField('self',  related_name='win_source', 
                                                    blank=True,
                                                    unique=True,
                                                    null=True,
                                                    verbose_name='Winner goes to',
                                                    help_text='Leave blank for Finals')

    loser_matchup   = models.OneToOneField('self',  related_name='lose_source',
                                                    blank=True,
                                                    unique=True,
                                                    null=True,
                                                    verbose_name='Loser goes to',
                                                    help_text='Leave blank if loser is eliminated')


    # FIXME: Matchup with this Player 1 already exists.
    player_1 = models.OneToOneField('players.Player',   blank=True,
                                                        null=True,
                                                        related_name='player_1',
                                                        verbose_name='Player 1',
                                                        help_text='Only set for first round matches')

    player_2 = models.OneToOneField('players.Player',   blank=True,
                                                        null=True,
                                                        related_name='player_2',
                                                        verbose_name='Player 2',
                                                        help_text='Only set for first round matches')
    
    def __str__(self):
        if self.player_1_id:
            player_1_name = self.player_1.name
        else:
            player_1_name = '???'

        if self.player_2_id:
            player_2_name = self.player_2.name
        else:
            player_2_name = '???'

        return "%s: %s vs. %s" % (self.name,player_1_name,player_2_name)
