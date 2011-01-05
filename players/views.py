import json
from django.http import HttpResponse
from ladder_viewer.lib.sc2ranks.sc2ranks import Sc2Ranks

def sc2ranks(request):
    client = Sc2Ranks('GSAR tournament')

    multiple_profiles = False

    if len(request.GET['charcode']) > 0:
        code = request.GET['charcode']
    else:
        try:
            profiles = client.search_for_profile(region='us', name=request.GET['name'])
            profile = profiles[0]
            if len(profiles) > 1:
                multiple_profiles = True
        except:
            return HttpResponse(json.dumps({
                'error':    'Profile not found'
            }))
        code = profile.character_code
        

    try:
        character_teams = client.fetch_base_character_teams(
            region  = 'us',
            name    = request.GET['name'],
            code    = code
        )
    except:
        return HttpResponse(json.dumps({
            'error': 'Profile not found'
        }));

    if character_teams.teams.has_key('1v1'):
        league  = character_teams.teams['1v1'].league
        race    = character_teams.teams['1v1'].fav_race
    else:
        league  = ''
        race    = ''

    response = {
        'name':     request.GET['name'],
        'bnet_id':  character_teams.bnet_id,
        'charcode': character_teams.character_code,
        'league':   league,
        'race':     race,
        'portrait': {
            'id':   character_teams.portrait.icon_id,
            'row':  character_teams.portrait.row,
            'col':  character_teams.portrait.column
        }
    }

    if multiple_profiles:
        response['warning'] = 'WARNING: Multiple profiles returned. Specify character code and try again'

    return HttpResponse(json.dumps(response))
