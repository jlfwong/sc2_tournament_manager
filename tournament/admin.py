from django.contrib import admin
from ladder_viewer.tournament.models import Matchup
from ladder_viewer.players.models import Player
from django import forms
from django.db.models import Q
from django.utils.functional import curry

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
    select_related = True

    list_display = (
        'name',
        'winner_matchup',
        'loser_matchup',
        'player_1',
        'player_2',
        'winner',
    )

    list_editable = (
        'winner_matchup',
        'loser_matchup',
        'player_1',
        'player_2',
        'winner',
    )

    radio_fields = {'winner':admin.HORIZONTAL}

    def change_view(self, *args, **kwargs): 
        self.fieldsets = (
            (None, {
                'fields': ('name',)
            }),
            ('Results', {
                'fields': ('winner',)
            }),
            ('Aftermath', {
                'fields': ('winner_matchup','loser_matchup',)
            }),
            ('Players', {
                'fields': ('player_1', 'player_2',)
            }),
        )
        return super(MatchupAdmin, self).change_view(*args,**kwargs)

    def add_view(self, *args, **kwargs):
        self.fieldsets = (
            (None, {
                'fields': ('name',)
            }),
            ('Aftermath', {
                'fields': ('winner_matchup','loser_matchup',),
            }),
            ('Players', {
                'fields': ('player_1', 'player_2',)
            }),
        )
        return super(MatchupAdmin, self).add_view(*args,**kwargs)
        
    # Use MatchupAdminForm for changelist as well
    get_changelist_form = curry(admin.ModelAdmin.get_changelist_form,form=MatchupAdminForm)

admin.site.register(Matchup,MatchupAdmin)
