from django.contrib import admin
from ladder_viewer.tournament.models import Matchup
from ladder_viewer.players.models import Player
from django import forms
from django.db.models import Q

class MatchupAdminForm(forms.ModelForm):
    def __init__(self,*args,**kwargs):
        """ Limit the choices of winner to the players in the match """
        super(MatchupAdminForm,self).__init__(*args,**kwargs)

        if self.fields.has_key('winner'):
            matchup = self.instance
            q = Q(id=-1)
            if matchup.player_1_id:
                q = q | Q(id=matchup.player_1.id)
            if matchup.player_2_id:
                q = q | Q(id=matchup.player_2.id)

            self.fields['winner'].queryset=Player.objects.filter(q)

    class Meta: pass

class MatchupAdmin(admin.ModelAdmin):
    model = Matchup
    form = MatchupAdminForm


    def change_view(self, *args, **kwargs): 
        self.fieldsets = (
            (None, {
                'fields': ('name',)
            }),
            ('Results', {
                'fields': ('winner',)
            }),
            ('Players', {
                'fields': ('player_1', 'player_2',)
            }),
            ('Aftermath', {
                'fields': ('winner_matchup','loser_matchup',)
            }),
        )
        return super(MatchupAdmin, self).change_view(*args,**kwargs)

    def add_view(self, *args, **kwargs):
        self.fieldsets = (
            (None, {
                'fields': ('name',)
            }),
            ('Players', {
                'fields': ('player_1', 'player_2',)
            }),
            ('Aftermath', {
                'fields': ('winner_matchup','loser_matchup',),
            }),
        )
        return super(MatchupAdmin, self).add_view(*args,**kwargs)

admin.site.register(Matchup,MatchupAdmin)
