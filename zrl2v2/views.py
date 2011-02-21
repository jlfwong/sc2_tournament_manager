import os
from django.http import HttpResponse
import hashlib
import simplejson
# Create your views here.

DATA_JSON_PATH = os.path.join(os.path.dirname(__file__),"data.json")


def data_handle(request):
    if 'data' in request.POST and request.session.get('2v2_authed',False):
        data_json = request.POST['data']
        simplejson.loads(data_json) # Sanity check
        open(DATA_JSON_PATH,'w').write(data_json)
    else:
        data_json = open(DATA_JSON_PATH).read()
    return HttpResponse(data_json,mimetype="application/json")

def auth(request):
    salt = '1098aodj198shodkjasd'
    password = request.POST.get('password','')
    h = hashlib.sha224(password + salt).hexdigest()
    if h == '47843b02839d4a250ca98aaa892a37fc83a7c9434904abe959ab38dd':
        request.session['2v2_authed'] = True
        response = 'ok'
    else:
        response = 'Invalid Password'
    return HttpResponse(response,mimetype="text/plain")
