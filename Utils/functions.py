import json
from datetime import datetime
import datetime

import discord

# config
def dc_token():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["DC-Token"]


def db_token():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["DB-Token"]


def time_syntax():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Time-Syntax"]


def bot_data():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Bot"]


def files():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Files"]


def prefix():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Prefix"]


def cooldown():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Cooldown"]


def developer():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Developer-ID"]


def color():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Color"]


def version():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Version"]


def status_timeout():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Status-Timeout"]


def status():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Status"]


def chop_icon():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Chop-Icon"]


def cross_icon():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["Cross-Icon"]


def agc_webhook_deletion():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["AGC_Webhook_Deletion"]


def agc_webhook_edit():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["AGC_Webhook_Edit"]


def agc_webhook_vc():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["AGC_Webhook_VC"]


def agc_webhook_memberevent():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["AGC_Webhook_Memberevent"]


def agc_webhook_memberedit():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["AGC_Webhook_Memberedit"]


def agc_webhook_server():
    with open(r'Data/config.json', 'r') as f:
        config = json.load(f)
        return config["AGC_Webhook_Server"]


def getapiurl(ctx):
    with open(r'Data/config.json', 'r') as f:
        apiurlcfg = json.load(f)
        apiurl = apiurlcfg["KawaiiAPIUrl"]
    with open(r'Data/config.json', 'r') as f:
        apikeycfg = json.load(f)
        apikey = apikeycfg["KawaiiAPIToken"]
    with open(r'Data/config.json', 'r') as f:
        apitypecfg = json.load(f)
        apitype = apitypecfg["KawaiiAPIType"]
    return f"{apiurl}{ctx.command.name}/token={apikey}&type={apitype}"

def PSQLHost():
    with open(r'Data/config.json', 'r') as f:
        psqlhost = json.load(f)
        psqlhost = psqlhost["PSQLHost"]
        return psqlhost

def PSQLPass():
    with open(r'Data/config.json', 'r') as f:
        psqlhost = json.load(f)
        psqlhost = psqlhost["PSQLPass"]
        return psqlhost

def PSQLDB():
    with open(r'Data/config.json', 'r') as f:
        psqlhost = json.load(f)
        psqlhost = psqlhost["PSQLDB"]
        return psqlhost

def PSQLUser():
    with open(r'Data/config.json', 'r') as f:
        psqlhost = json.load(f)
        psqlhost = psqlhost["PSQLUser"]
        return psqlhost

def agc_check(ctx=None, req=None, event=None):
    server_id = 750365461945778209

    if event == True:
        if req == server_id:
            return True
        return False

    elif event == False:
        if ctx.guild.id == server_id:
            return True
        return False





def guild_embedcolor_ctx(self, ctx):
    try:
        self.bot.cursor.execute(
            f"SELECT color FROM embedcolor WHERE gid = '{ctx.guild.id}'")
        result = self.bot.cursor.fetchone()[0]

        return int(result, base=16)
    except:
        return color_data()


def guild_embedcolor_message(self, message):
    try:
        self.bot.cursor.execute(
            f"SELECT color FROM embedcolor WHERE gid = '{message.guild.id}'")
        result = self.bot.cursor.fetchone()[0]

        return int(result, base=16)
    except:
        return color_data()


def guild_embedcolor_message_guild(self, guild):
    try:
        self.bot.cursor.execute(
            f"SELECT color FROM embedcolor WHERE gid = '{guild.id}'")
        result = self.bot.cursor.fetchone()[0]

        return int(result, base=16)
    except:
        return color_data()


def guild_embedcolor_member(self, member):
    try:
        self.bot.cursor.execute(
            f"SELECT color FROM embedcolor WHERE gid = '{member.guild.id}'")
        result = self.bot.cursor.fetchone()[0]

        return int(result, base=16)
    except:
        return color_data()

# color data
def color_data():
    return discord.Color.from_rgb(color()[0], color()[1], color()[2])


