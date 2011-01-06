from django.contrib import admin
from ladder_viewer.tournament.models import Slot, Matchup
from ladder_viewer.players.models import Player
from django import forms
from django.db.models import Q

class SlotInline(admin.StackedInline):
    model = Slot
    max_num = 2
    can_delete = False

class MatchupAdminForm(forms.ModelForm):

    def __init__(self,*args,**kwargs):
        """ Limit the choices of winner to the players in the match """
        super(MatchupAdminForm,self).__init__(*args,**kwargs)
        q = Q()
        for slot in self.instance.slot_set.all():
            q = q | Q(slot=slot)

        self.fields['winner'].queryset=Player.objects.filter(q)

class MatchupAdmin(admin.ModelAdmin):
    model = Matchup
    inlines = [SlotInline]
    form = MatchupAdminForm

    def save_formset(self, request, form, formset, change):
        for slot_form in formset.forms:
            if slot_form.instance.pk: continue
            slot_form.instance.matchup = form.instance
            slot_form.save()

        return super(MatchupAdmin,self).save_formset(request,form,formset,change)

admin.site.register(Matchup,MatchupAdmin)
