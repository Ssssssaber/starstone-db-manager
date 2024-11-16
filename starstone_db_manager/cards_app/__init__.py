import logging
import datetime
import os

def setup_logger():
    time = datetime.datetime.now().isoformat().replace(":","-")
    
    filename = f"logs/{time}.txt"
    logging.basicConfig(filename=filename,
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    datefmt='%H:%M:%S',
                    level=logging.DEBUG)

setup_logger()
