from django.db import models

def has_changed(instance, field):
    if not instance.pk:
        return False
    old_value = instance.__class__._default_manager.\
             filter(pk=instance.pk).values(field).get()[field]
    return not getattr(instance, field) == old_value

class Matchup(models.Model):
    name        = models.CharField(max_length=30)
    winner      = models.ForeignKey('players.player',blank=True,null=True)

    winner_matchup  = models.ForeignKey('self',     related_name='win_source', 
                                                    blank=True,
                                                    null=True,
                                                    verbose_name='Winner goes to',
                                                    help_text='Leave blank for Finals')

    loser_matchup   = models.ForeignKey('self',     related_name='lose_source',
                                                    blank=True,
                                                    null=True,
                                                    verbose_name='Loser goes to',
                                                    help_text='Leave blank if loser is eliminated')


    # FIXME: Matchup with this Player 1 already exists.
    player_1 = models.ForeignKey('players.Player',      blank=True,
                                                        null=True,
                                                        related_name='player_1',
                                                        verbose_name='Player 1',
                                                        help_text='Only set for first round matches')

    player_2 = models.ForeignKey('players.Player',      blank=True,
                                                        null=True,
                                                        related_name='player_2',
                                                        verbose_name='Player 2',
                                                        help_text='Only set for first round matches')
    
    def participants(self):
        ret = []
        if self.player_1_id:
            ret += [self.player_1]
        if self.player_2_id:
            ret += [self.player_2]
        return ret

    def participant_ids(self):
        ret = []
        if self.player_1_id:
            ret += [self.player_1_id]
        if self.player_2_id:
            ret += [self.player_2_id]
        return ret

    def __getattr__(self,name):
        if name == 'loser':
            if self.winner_id:
                if self.winner == self.player_1:
                    return self.player_2
                else:
                    return self.player_1
            else:
                return None
        elif name == 'loser_id':
            if self.loser == None:
                return self.loser.id
            else:
                return None
        else:
            super(Matchup,self).__getattr(name)

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

    def save(self):
        super(Matchup,self).save()

        if self.winner_id and self.winner_matchup_id:
            winner_matchup = self.winner_matchup

            # Winner already propogated
            if winner_matchup.player_1_id == self.winner.id:
                return
            if winner_matchup.player_2_id == self.winner.id:
                return

            # Winner changed, remove the loser from the slots
            if winner_matchup.player_1_id == self.loser.id:
                winner_matchup.player_1 = None
            elif winner_matchup.player_2_id == self.loser.id:
                winner_matchup.player_2 = None

            # Propogate the winner
            if winner_matchup.player_1_id == None:
                winner_matchup.player_1 = self.winner
            elif winner_matchup.player_2_id == None:
                winner_matchup.player_2 = self.winner
            else:
                raise Exception('Cannot propogate winner')

            winner_matchup.save()

    class Meta:
        ordering = ['name']
