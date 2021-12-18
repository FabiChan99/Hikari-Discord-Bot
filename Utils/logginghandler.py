from Utils.imports import coloredlogs, logging
from datetime import datetime
import datetime


coloredlogs.install(fmt='\u001b[34m[%(asctime)s] \u001b[31m[%(levelname)s] \u001b[37m%(message)s')


# Discord Database Logger
discordlogger = logging.getLogger('discord')
handler = logging.FileHandler(filename=f'Logs/Discord/{datetime.datetime.utcnow().strftime("%d-%m-%Y")}.log', encoding='utf-8',
                              mode='a+')
handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
discordlogger.addHandler(handler)

## PostgreSQL Database Logger
#psycopg2 = logging.getLogger('psycopg2')
#psycopg2.setLevel(logging.DEBUG)
#handler = logging.FileHandler(filename=f'Logs/PostgreSQL/{datetime.datetime.utcnow().strftime("%d-%m-%Y")}.log', encoding='utf-8',
#                              mode='a+')
#handler.setFormatter(logging.Formatter('[%(asctime)s] [%(levelname)s] %(message)s'))
#psycopg2.addHandler(handler)
