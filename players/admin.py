from django.contrib import admin
from ladder_viewer.players.models import Player
from django import forms
from django.template import Template, Context
from django.utils.safestring import mark_safe

class Sc2RanksWidget(forms.TextInput):
    def render(self, name, value, attrs=None):
        text_input = super(Sc2RanksWidget,self).render(name,value,attrs)
        tpl = Template("""{{text_input}} <input type='button' value='Load from SC2Ranks' data-sc2ranks-button=1/>""")
        return mark_safe(tpl.render(Context({'text_input':text_input})))

class PlayerAdminForm(forms.ModelForm):
    name = forms.CharField(widget=Sc2RanksWidget)

    class Meta:
        model = Player
        fields = (
            'name',
            'charcode',
            'league',
            'race',
            'bnet_id',
            'portrait_id',
            'portrait_row',
            'portrait_col',
        )

    class Media:
        js = (
            'https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js',
            'js/admin_player.js',
        )


class PlayerAdmin(admin.ModelAdmin):
    form = PlayerAdminForm
    list_display = ('name','charcode','league')

admin.site.register(Player,PlayerAdmin)
