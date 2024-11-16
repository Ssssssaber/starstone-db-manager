from django.shortcuts import HttpResponse
from starstone_db_manager.settings import NATIVE_MYSQL_DATABASES
# Create your views here.
import pymysql.cursors
import json
from django.views.decorators.csrf import csrf_exempt

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

    
    # check downloadAll

    # return process_download_all(request, cardData)
    
    # check download
    
    # if not request.POST._mutable:
    #     request.POST._mutable = True
    # request.POST["id"] = 26
    # return process_download(request, cardData)   

    # check upload

    # if not request.POST._mutable:
    #     request.POST._mutable = True
    # request.POST["request-type"] = "Upload"
    # request.POST["name"] = "bad"
    # request.POST["desc"] = ""
    # request.POST["mana-cost"] = ""
    # request.POST["health"] = ""
    # request.POST["attack"] = ""
    # request.POST["race"] = ""
    # request.POST["card-type"] = ""
    # request.POST["play-style"] = ""
    # return process_upload(request, cardData)
    
    # check delete


    # print(get_autoincrement())

    # if not request.POST._mutable:
    #     request.POST._mutable = True
    
    # request.POST["id"] = 26
    # return process_delete(request, cardData)   

    # query = """SELECT * FROM starstoneapp.cardstats"""
    # r = execute(NATIVE_MYSQL_DATABASES['default'], query, {})
 
    # cardData["cardStats"] = []
    # for card in r:
    #     cardData["cardStats"].append(card_stats_from_query(card))
    # return HttpResponse(json.dumps(cardData))
    # print(request)

    if not request.method == "POST":
        set_error(cardData, "waiting for POST request")
        return HttpResponse(json.dumps(cardData))

    if not "request-type" in request.POST:
        set_error(cardData, "request type was not specified")
        return HttpResponse(json.dumps(cardData))
        
    request_type = request.POST.get("request-type")

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

def get_card_by_id(i):
    query = """SELECT * FROM starstoneapp.cardstats WHERE id = %(card_id)s;"""
    params = {
        "card_id": i
    }
    r = execute(NATIVE_MYSQL_DATABASES['default'], query, params)
    
    if (r == []):
        return None

    return card_stats_from_query(r[0])

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

def card_stats_from_query(query):

    cardStats = {}
    cardStats["id"] = query[0]
    cardStats["Name"] = query[1]
    cardStats["Desc"] = query[2]
    cardStats["Health"] = query[3]
    cardStats["ManaCost"] = query[5]
    cardStats["Attack"] = query[6]
    cardStats["Race"] = query[7]
    cardStats["Type"] = query[8]
    cardStats["PlayStyle"] = query[9]
    
    return cardStats

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
        error = insert(NATIVE_MYSQL_DATABASES['default'], query, params)
        if (error != None):
                set_error(cardData, error) 

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

def execute(database_dict: dict, query: str, params: dict) -> list[tuple]:
    connection = pymysql.connect(**database_dict)
    cursor = connection.cursor()
    # cursor.reset()
    cursor.execute(query, params)
    r = cursor.fetchall()
    connection.close()

    return r

def insert(database_dict: dict, query: str, params: dict) -> None:
    connection = pymysql.connect(**database_dict)
    cursor = connection.cursor()
    message = ""
    try:
        cursor.execute(query, params)
        connection.commit()
        connection.close()
        return None
    except Exception as e:
        connection.rollback()
        connection.close()
        if hasattr(e, 'message'):
            return e.message
        else:
            return str(e)


    

def set_error(cardData: dict, error_text : str) -> None:
    cardData["cardStats"] = None;
    cardData["error"]["isError"] = True;
    cardData["error"]["errorText"] = "Error: " + error_text;
