import pymysql.cursors
import logging
from starstone_db_manager.settings import NATIVE_MYSQL_DATABASES

logger = logging.getLogger(__name__)

def get_autoincrement():
    query = """SELECT MAX(Id) as id FROM starstoneapp.cardstats;"""
    r = execute(NATIVE_MYSQL_DATABASES['default'], query, {})
    return int(r[0][0])

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


def get_card_by_id(i):
    query = """SELECT * FROM starstoneapp.cardstats WHERE id = %(card_id)s;"""
    params = {
        "card_id": i
    }
    r = execute(NATIVE_MYSQL_DATABASES['default'], query, params)
    
    if (len(r) == 0):
        return None

    return card_stats_from_query(r[0])



def execute(database_dict: dict, query: str, params: dict) -> list[tuple]:
    connection = pymysql.connect(**database_dict)
    cursor = connection.cursor()
    # cursor.reset()
    try:
        logger.info(f'Preforming query {query} with {params}')
        cursor.execute(query, params)
        r = cursor.fetchall()
        connection.close()
    except Exception as e:
        connection.close()
        if hasattr(e, 'message'):
            logger.error(e.message)
            return e.message
        else:
            logger.error(str(e))
            return str(e)

    return r

def insert(database_dict: dict, query: str, params: dict) -> None:
    connection = pymysql.connect(**database_dict)
    cursor = connection.cursor()
    message = ""
    try:
        logger.info(f'Preforming query {query} with {params}')
        cursor.execute(query, params)
        connection.commit()
        connection.close()
        return None
    except Exception as e:
        connection.rollback()
        connection.close()
        if hasattr(e, 'message'):
            logger.error(e.message)
            return e.message
        else:
            logger.error(str(e))
            return str(e)

