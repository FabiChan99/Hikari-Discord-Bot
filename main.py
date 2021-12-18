import asyncio

from Utils.data import *

from discord.ext import commands
from discord.ext.commands import CommandNotFound, MissingPermissions, MessageNotFound
from Utils.functions import color_data, cross_icon
from Utils.imports import random
import discord
import time
from discord.ext import commands


# get prefix
def get_prefix(bot, message):
    # return "h!"
    if not message.guild:
        return commands.when_mentioned_or("h!")(bot, message)
    prefix_uwu = prefix_data(message.guild.id)
    if prefix_uwu.lower() == "h!":
        return commands.when_mentioned_or("h!")(bot, message)
    else:
        return commands.when_mentioned_or(prefix_uwu)(bot, message)


# setup bot class
class Hikari(commands.AutoShardedBot):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


intents = discord.Intents.default()
intents.members = True
intents.guilds = True
bot = Hikari(
    command_prefix=get_prefix,
    chunk_guilds_at_startup=True,
    case_insensitive=True,
    activity=discord.Streaming(name='Starting Bot...', url='https://twitch.tv/#'),
    owner_id=developer(),
    intents=intents,
    help_command=None,
    max_messages=15000)

print(f'[{datetime.datetime.now().strftime(time_syntax())}][INFO] Booting Up...')

try:
    # Connect to an existing database
    bot.connection = connection = psycopg2.connect(user=PSQLUser(),
                                                   password=PSQLPass(),
                                                   host=PSQLHost(),
                                                   database=PSQLDB())

    # Create a cursor to perform database operations
    bot.cursor = bot.connection.cursor()
    bot.cursor.execute("SELECT version();")
    # Fetch result
    record = bot.cursor.fetchone()
    print("You are connected to - ", record, "\n")

except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)

bot.load_extension("jishaku")

togetherControl = DiscordTogether(bot)


@bot.event
async def on_ready():
    bot.loop.create_task(status_task(bot))
    bot.togetherControl = DiscordTogether(bot.http.token)
    bot.userAgentHeaders = {'User-Agent': f'linux:hikari-discordbot'}
    print('\u001b[35mBot information:')
    print(f' Name: {bot.user.name}')
    print(f' ID: {bot.user.id}')
    print(f' Developer: {bot.get_user(developer())}')
    print(f' Version: {version()}')
    print(f' Guilds: {len(bot.guilds)}')
    print(f' Shards: {bot.shard_count}')
    print(f' Users: {sum(g.member_count for g in bot.guilds)}')
    for filename in os.listdir('Cogs'):
        if filename.endswith('.py'):
            try:
                bot.load_extension(f'Cogs.{filename[:-3]}')
                loaded_cogs(str(filename[:-3]))
                print(
                    f"\033[94m[{datetime.datetime.now().strftime(time_syntax())}][INFO] The file {filename[:-3]} was loaded\u001b[0m")
            except Exception as e:
                raise e
    loaded_cogs('end')


async def status_task(bot):
    while True:
        try:
            await bot.change_presence(activity=discord.Game(
                name=f"h!help | Guilds: {len(bot.guilds)} | Shards: {len(bot.shards)} | Version {(version())}"))
            await asyncio.sleep(status_timeout())
        except Exception:
            pass


# error handler
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, CommandNotFound):
        embed = discord.Embed(color=color_data())
        embed.set_author(name=f"Command not found!", icon_url=cross_icon())
        embed.add_field(name=f'> Information:', value=f'Sorry but this command doesn\'t exist.')
        msg = await ctx.message.reply(embed=embed, mention_author=False)
        await asyncio.sleep(10)
        await ctx.message.delete()
        await msg.delete()
        return
    if isinstance(error, MessageNotFound):
        return
    if isinstance(error, PermissionError):
        embed = discord.Embed(color=color_data())
        embed.set_author(name=f"Missing Permissions!", icon_url=cross_icon())
        embed.add_field(name=f'> Information:', value=f'Sorry but i don\'t have enough permissions to do that')
        await ctx.message.reply(embed=embed, mention_author=False)
        return
    if isinstance(error, MissingPermissions):
        embed = discord.Embed(color=color_data())
        embed.set_author(name=f"Missing Permissions!", icon_url=cross_icon())
        embed.add_field(name=f'> Information:', value=f'Sorry, You don\'t have enough permissions to do this')
        await ctx.message.reply(embed=embed, mention_author=False)
        return
    if isinstance(error, RuntimeError):
        embed = discord.Embed(color=color_data())
        embed.set_author(name=f"Runtime error!", icon_url=cross_icon())
        embed.add_field(name=f'> Information:', value=f'Something took to long please try again')
        await ctx.message.reply(embed=embed, mention_author=False)
        return
    if isinstance(error, commands.BadArgument):
        embed = discord.Embed(color=color_data())
        embed.set_author(name=f"Bad argument!", icon_url=cross_icon())
        embed.add_field(name=f'> Info:', value='Please make sure that the arguments you provide are correct')
        await ctx.message.reply(embed=embed, mention_author=False)
        return
    if isinstance(error, commands.CommandOnCooldown):
        embed = discord.Embed(color=random.choice([0xFF4D4D, 0xDB3846, 0xB7263F]))
        embed.set_author(name=f"Please wait before using the command again!", icon_url=ctx.author.avatar.url)
        embed.add_field(name=f'How long do I have to wait?',
                        value='You will have to wait `{} seconds` '
                              'before using `{}` again.'.format(
                            round(error.retry_after, 1), ctx.command.name))
        await ctx.message.reply(embed=embed, mention_author=False)
        return
    else:
        raise error



async def on_message(message):
    if message.author.bot:
        return
    await bot.process_commands(message)


@bot.command(pass_context=True)
async def reload(ctx, *, msg):
    if ctx.author.id == 591226486657253377:
        try:
            if os.path.exists("Cogs/{}.py".format(msg)):
                bot.reload_extension("Cogs.{}".format(msg))
            elif os.path.exists("Cogs/{}.py".format(msg)):
                bot.reload_extension("Cogs.{}".format(msg))
            else:
                raise ImportError("No module named '{}'".format(msg))
        except Exception as e:
            await ctx.send('Failed to reload module: `{}.py`'.format(msg))
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('Reloaded module: `{}.py`'.format(msg))
            print('Reloaded module: {}.py'.format(msg))


@bot.command()
async def restart(ctx):
    if ctx.author.id == 591226486657253377:
        color = color_data()
        MSG = "Closing Eventloop"
        embed = discord.Embed(description=MSG, color=color)
        asyncio.get_event_loop()
        kek = await ctx.send(embed=embed)
        MSG = "Restarting..."
        embed = discord.Embed(description=MSG, color=color)
        await asyncio.sleep(3)
        await kek.edit(embed=embed)
        os.system(f"taskkill /PID {os.getpid()} /F")


@bot.command(pass_context=True)
async def unload(ctx, *, msg):
    if ctx.author.id == 591226486657253377:
        try:
            if os.path.exists("Cogs/{}.py".format(msg)):
                bot.unload_extension("Cogs.{}".format(msg))
            elif os.path.exists("Cogs/{}.py".format(msg)):
                bot.unload_extension("Cogs.{}".format(msg))
            else:
                raise ImportError("No module named '{}'".format(msg))
        except Exception as e:
            await ctx.send('Failed to unload module: `{}.py`'.format(msg))
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('Unloaded module: `{}.py`'.format(msg))


@bot.command(pass_context=True)
async def load(ctx, *, msg):
    if ctx.author.id == 591226486657253377:
        try:
            if os.path.exists("Cogs/{}.py".format(msg)):
                bot.load_extension("Cogs.{}".format(msg))
            elif os.path.exists("Cogs/{}.py".format(msg)):
                bot.load_extension("Cogs.{}".format(msg))
            else:
                raise ImportError("No module named '{}'".format(msg))
        except Exception as e:
            await ctx.send('Failed to load module: `{}.py`'.format(msg))
            await ctx.send('{}: {}'.format(type(e).__name__, e))
        else:
            await ctx.send('Loaded module: `{}.py`'.format(msg))


bot.run(dc_token())
