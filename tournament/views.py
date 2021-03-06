from django.shortcuts import render_to_response
from players.models import Player
from models import Matchup
from django.contrib.auth.decorators import login_required

def home(request):
    return render_to_response('index.html',{
        'matchup_list' : Matchup.objects.all()
    })
    
@login_required
def players(request):
    return render_to_response('players.html',{
        'player_list': Player.objects.all()
    })
