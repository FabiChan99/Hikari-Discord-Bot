# imports

from Utils.functions import *
from Utils.imports import *
from Utils.logginghandler import *




# define Bot Boot time
start_time = datetime.datetime.now()

# Discord Debug Log Handler


# database functions
cluster = MongoClient(db_token())
db = cluster["hikari"]
prefix_db = db[f"{bot_data()}-guilds"]


def prefix_data(guild_id):
    try:
        guilds = prefix_db.find_one({"_id": int(guild_id)})
        prefix_get = guilds["prefix"]
    except Exception:
        prefix_get = prefix()
    return prefix_get


def setup_guild(guild):
    if not guild:
        return
    guilds = prefix_db.find_one({"_id": int(guild.id)})
    if not guilds:
        prefix_db.insert_one({"_id": int(guild.id),
                              "prefix": str(prefix())})


# converter for system metrics
def converter(data):
    symbols = ('K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y')
    prefix_a = {}
    for i, s in enumerate(symbols):
        prefix_a[s] = 1 << (i + 1) * 10
    for s in reversed(symbols):
        if data >= prefix_a[s]:
            value = float(data) / prefix_a[s]
            return '%.1f%s' % (value, s)
    return "%sB" % data

load_data= []

# load cogs
def loaded_cogs(cog):
    load_data.append(cog)
    if len(load_data) == files() + 1:
        print(
            f'\n\u001b[32m[{datetime.datetime.now().strftime(time_syntax())}][INFO] Loaded {len(load_data) - 1}/{files()} files\u001b[0m')
        print(f'\u001b[32m[{datetime.datetime.now().strftime(time_syntax())}][INFO] Connected to Discord\u001b[0m')
        print(f'\u001b[32m[{datetime.datetime.now().strftime(time_syntax())}][INFO] The Bot is online\u001b[0m')
