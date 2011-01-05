from django.contrib import admin
from ladder_viewer.players.models import Player
from django import forms

class PlayerAdminForm(forms.ModelForm):
    class Meta:
        model = Player

    class Media:
        js = ('js/admin_player.js',)

class PlayerAdmin(admin.ModelAdmin):
    form = PlayerAdminForm

admin.site.register(Player,PlayerAdmin)
