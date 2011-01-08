from django.db import models
from lib import tournament_tree

class Matchup(models.Model):
    name        = models.CharField(max_length=30)
    winner      = models.ForeignKey('players.player',   blank=True,
                                                        null=True,
                                                        related_name='won')

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
    @property 
    def display_coords(self):
        return tournament_tree.mapping[self.name]

    def get_display_coords(self,field):
        if self.display_coords.has_key(field):
            return {
                'left'  : self.display_coords[field][0],
                'top'   : self.display_coords[field][1]
            }
        else:
            return None

    def player_1_coords(self):
        return self.get_display_coords('player_1')

    def player_2_coords(self):
        return self.get_display_coords('player_2')

    def winner_coords(self):
        return self.get_display_coords('winner')

    def loser_coords(self):
        return self.get_display_coords('loser')

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

    @property
    def loser(self):
        if self.winner_id:
            if self.winner == self.player_1:
                return self.player_2
            else:
                return self.player_1
        else:
            return None

    @property
    def loser_id(self):
        if self.loser == None:
            return None
        else:
            return self.loser.id

    def __str__(self):
        return self.name

    def save(self):
        super(Matchup,self).save()

        if self.winner_id:
            if self.winner_matchup_id:
                winner_matchup = self.winner_matchup

                # Winner already propogated
                if winner_matchup.player_1_id == self.winner.id:
                    return
                if winner_matchup.player_2_id == self.winner.id:
                    return

                # Winner changed, remove the loser from the slots
                if winner_matchup.player_1_id == self.loser_id:
                    winner_matchup.player_1 = None
                elif winner_matchup.player_2_id == self.loser_id:
                    winner_matchup.player_2 = None

                # Propogate the winner
                if winner_matchup.player_1_id == None:
                    winner_matchup.player_1 = self.winner
                elif winner_matchup.player_2_id == None:
                    winner_matchup.player_2 = self.winner
                else:
                    raise Exception('Cannot propogate winner')

                winner_matchup.save()

        if self.loser_id:
            if self.loser_matchup_id:
                loser_matchup = self.loser_matchup
    
                # Loser already propogated
                if loser_matchup.player_1_id == self.loser_id:
                    return
                if loser_matchup.player_2_id == self.loser_id:
                    return

                # Loser changed, remove the winner from the slots
                if loser_matchup.player_1_id == self.winner_id:
                    loser_matchup.player_1 = None
                if loser_matchup.player_2_id == self.winner_id:
                    loser_matchup.player_2 = None

                # Propogate the loser
                if loser_matchup.player_1_id == None:
                    loser_matchup.player_1 = self.loser
                elif loser_matchup.player_2_id == None:
                    loser_matchup.player_2 = self.loser
                else:
                    raise Exception('Cannot propogate loser')

                loser_matchup.save()
                    


    class Meta:
        ordering = ['name']
