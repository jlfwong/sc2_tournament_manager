from django.contrib import admin
from ladder_viewer.tournament.models import Slot, Matchup

class SlotInline(admin.StackedInline):
    model = Slot
    max_num = 2
    can_delete = False

class MatchupAdmin(admin.ModelAdmin):
    model = Matchup
    inlines = [SlotInline]

    def save_formset(self, request, form, formset, change):
        #import pdb; pdb.set_trace()
        #import IPython; IPython.ipapi.launch_new_instance(locals())
        for slot_form in formset.forms:
            if slot_form.instance.pk: continue
            slot_form.instance.matchup = form.instance
            slot_form.save()

        return super(MatchupAdmin,self).save_formset(request,form,formset,change)
            

admin.site.register(Matchup,MatchupAdmin)
