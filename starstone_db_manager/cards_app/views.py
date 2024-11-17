from django.shortcuts import HttpResponse
from starstone_db_manager.settings import NATIVE_MYSQL_DATABASES
from .db_queries import get_autoincrement, get_card_by_id, execute, insert, card_stats_from_query
# Create your views here.
import pymysql.cursors
import json
from django.views.decorators.csrf import csrf_exempt
import logging 

logger = logging.getLogger(__name__)

from enum import Enum

# class syntax

class Type(Enum):
    Creature = 1
    Spell = 2

class Race(Enum):
    Terran = 1
    Zerg = 2
    Protoss = 3

class PlayStyle(Enum):
    Offensive = 1
    Defensive = 2
    Versatile = 3

def check_type(poss_type, enum_class):
    try:
        keke = enum_class[poss_type]
        return True
    except Exception as e:
        return False

@csrf_exempt
def main_manage_page(request):
    
    cardStats = {
        "id": 1,
        "Name": "Name",
        "Desc": "NULL"
    }

    error = {
        "errorText": "empty",
        "isError": False
    }

    cardData = {
        "cardStats": cardStats,
        "error": error
    }

    if not request.method == "POST":
        set_error(cardData, "waiting for POST request")
        return HttpResponse(json.dumps(cardData))

    if not "request-type" in request.POST:
        set_error(cardData, "request type was not specified")
        return HttpResponse(json.dumps(cardData))
        
    request_type = request.POST.get("request-type")
    log_request(request)

    if request_type == "DownloadAll":
        return process_download_all(request, cardData)
    elif request_type == "Download":
        return process_download(request, cardData)        
    elif request_type == "Upload":
        return process_upload(request, cardData)
    elif request_type == "Delete":
        return process_delete(request, cardData)
    else:
        set_error(cardData, f"Following request type is not supported {request_type}")
        return HttpResponse(json.dumps(cardData))

def log_request(request):
    logger.info(f"Receiveing request: {request.POST}")

def process_download_all(request, cardData):
    query = """SELECT * FROM starstoneapp.cardstats;"""
    r = execute(NATIVE_MYSQL_DATABASES['default'], query, {})
 
    cardData["cardStats"] = []
    for card in r:
        cardData["cardStats"].append(card_stats_from_query(card))
    return HttpResponse(json.dumps(cardData))

def process_download(request, cardData):
    if not "id" in request.POST:
        set_error(cardData, "Id was not set")
        return HttpResponse(json.dumps(cardData))

    card_id = request.POST.get("id")
    card = get_card_by_id(card_id);

    if card == None:
        set_error(cardData, f"card was not found with id: {card_id}")
        return HttpResponse(json.dumps(cardData)) 
        
    cardData["cardStats"] = card 
    return HttpResponse(json.dumps(cardData))

def check_for_valid_upload(request):
    form_params = [
        "request-type",
        "name",
        "desc",
        "mana-cost",
        "health",
        "attack",
        "race",
        "card-type",
        "play-style"
    ]

    error = "Following parameters are not set: "
    is_error = False
    for param in form_params:
        if not param in request.POST:
            is_error = True
            error += param + "; "
    return is_error, error

# check params
# get card
# delete card
# return cardstats
def process_delete(request, cardData):
    if not "id" in request.POST:
        set_error(cardData, "Id was not set")
        return HttpResponse(json.dumps(cardData))

    # select card from table
    card_id = request.POST.get("id")
    card = get_card_by_id(card_id);

    if card == None:
        set_error(cardData, f"card was not found with id: {card_id}")
        return HttpResponse(json.dumps(cardData)) 
    # set card
    cardData["cardStats"] = card
    
    query = """DELETE FROM starstoneapp.cardstats WHERE id = %(card_id)s;"""
    params = {
        "card_id": request.POST.get("id"),
    }
    # perform query
    error = insert(NATIVE_MYSQL_DATABASES['default'], query, params)
    if (error != None):
            set_error(cardData, error) 
    
    return HttpResponse(json.dumps(cardData))

def get_autoincrement():
    query = """SELECT MAX(Id) as id FROM starstoneapp.cardstats;"""
    r = execute(NATIVE_MYSQL_DATABASES['default'], query, {})
    return int(r[0][0])

# check params
# upload card
# get card and return

def process_upload(request, cardData):
    
    is_error, error = check_for_valid_upload(request)
    if (is_error):
        set_error(cardData, error)
        return HttpResponse(json.dumps(cardData))

    query = """SELECT * FROM starstoneapp.cardstats WHERE (Name = %(name)s) AND (Description = %(desc)s);"""
    params = {
        "name": request.POST.get("name"),
        "desc": request.POST.get("desc"),
    }
    
    r = execute(NATIVE_MYSQL_DATABASES['default'], query, params)
    #check what value is r when result is null
    if (len(r) == 0):
        query = """INSERT INTO starstoneapp.cardstats (Name, Description, ManaCost, Health, Attack, Race, Type, PlayStyle)\
VALUES (%(name)s, %(desc)s, %(mana-cost)s, %(health)s, %(attack)s, %(race)s, %(card-type)s, %(play-style)s);"""
        params = {
            "request-type": request.POST.get("request-type"),
            "name": request.POST.get("name"),
            "desc": request.POST.get("desc"),
            "mana-cost": request.POST.get("mana-cost"),
            "health": request.POST.get("health"),
            "attack": request.POST.get("attack"),
            "race": request.POST.get("race"),
            "card-type": request.POST.get("card-type"),
            "play-style": request.POST.get("play-style")
        }

        if not (check_type(params['race'], Race)):
            set_error(cardData, "Wrong race")
            return HttpResponse(json.dumps(cardData))
            
        if not (check_type(params['card-type'], Type)):
            set_error(cardData, "Wrong card type")
            return HttpResponse(json.dumps(cardData))

        if not (check_type(params['play-style'], PlayStyle)):
            set_error(cardData, "Wrong play style")
            return HttpResponse(json.dumps(cardData))

        error = insert(NATIVE_MYSQL_DATABASES['default'], query, params)
        if (error != None):
            set_error(cardData, error) 
            return HttpResponse(json.dumps(cardData))

        card_id = get_autoincrement()
        card = get_card_by_id(card_id)
        if card == None:
            set_error(cardData, f"card was not found with id: {card_id}")
            return HttpResponse(json.dumps(cardData)) 
        # set card
        cardData["cardStats"] = card
    else:
        set_error(cardData, "Card already exists")
    return HttpResponse(json.dumps(cardData))
   

def set_error(cardData: dict, error_text : str) -> None:
    cardData["cardStats"] = None;
    cardData["error"]["isError"] = True;
    cardData["error"]["errorText"] = "Error: " + error_text;
    logger.error(error_text)