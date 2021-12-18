# import

afkicon = "https://cdn.discordapp.com/attachments/836905275252408341/842816090434437160/StupidAFK.png"

from Utils.data import *

def get_afk_time(then):
    def to_human_time(input):
        min = 0
        h = 0
        d = 0
        while input >= 60:
            min += 1
            input -= 60
        sec = input
        while min >= 60:
            h += 1
            min -= 60
        while h >= 24:
            d += 1
            h -= 24
        return [sec, min, h, d]
    now = int(time.time())
    data = to_human_time(int(now) - int(then))
    string = ""
    if data[0] > 0 and data[1] == 0 and data[2] == 0 and data[3] == 0:
        string += str(data[0]) + "sec "
    if data[3] > 0:
        string += str(data[3]) + "days "
    if data[2] > 0:
        string += str(data[2]) + "hours "
    if data[1] > 0:
        string += str(data[1]) + "min "
    return string

# class
class Afk(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.cooldown(1, 10.0, commands.BucketType.user)
    @commands.bot_has_permissions(manage_nicknames=True)
    async def afk(self, ctx, *, reason=None):
        await ctx.message.add_reaction("<a:HikariLoading:822433462141190166>")
        afktime = int(time.time())
        await asyncio.sleep(1)
        if not reason:
            reason = "No reason provided"
            pass
        try:
            self.bot.cursor.execute(f"DELETE FROM afk WHERE gid = '{ctx.guild.id}' and userid = {ctx.author.id}")
            self.bot.connection.commit()
        except:
            pass
        sql = ("INSERT INTO afk(userid, reason, afktime, gid) VALUES(%s,%s,%s,%s)")
        val = (str(ctx.author.id), reason, afktime, str(ctx.guild.id))
        self.bot.cursor.execute(sql, val)
        self.bot.connection.commit()
        embed = discord.Embed(description=f"Okay {ctx.author.mention}, set your AFK to `{reason}`!", color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name="AFK System | Activated AFK mode", icon_url=afkicon)
        await ctx.message.reply(embed=embed, mention_author=False, delete_after=10)
        await ctx.message.delete()

    @commands.Cog.listener()
    async def on_message(self, message):




        if message.author.bot: return
        if message.mentions is not None:
            try:
                menid = message.mentions[0].id
            except: pass
            try:
                self.bot.cursor.execute(
                    f"SELECT userid FROM afk WHERE gid = '{message.guild.id}' and userid = '{menid}'")
                user = self.bot.cursor.fetchone()
                if user is not None:
                    self.bot.cursor.execute(
                        f"SELECT reason FROM afk WHERE gid = '{message.guild.id}' and userid = '{menid}'")
                    reason = self.bot.cursor.fetchone()
                    self.bot.cursor.execute(
                        f"SELECT afktime FROM afk WHERE gid = '{message.guild.id}' and userid = '{menid}'")
                    since = self.bot.cursor.fetchone()

                    embed = discord.Embed(description=f"{message.mentions[0]} is currently **AFK**: `{reason[0]}` - since `{get_afk_time(int(since[0]))}`", color=guild_embedcolor_message(self, message))
                    embed.set_author(name="AFK System | User is AFK", icon_url=afkicon)
                    await message.channel.send(embed=embed, delete_after=10)
            except IndexError:
                pass
            except UnboundLocalError:
                pass
        nick = message.author.nick
        try:
            if message.mentions is []: return
            if message.author.bot: return
            self.bot.cursor.execute(
                f"SELECT userid FROM afk WHERE gid = '{message.guild.id}' and userid = '{message.author.id}'")
            isafk = self.bot.cursor.fetchone()
        except IndexError:
            pass
        if isafk is None: return
        if isafk != None:
            self.bot.cursor.execute(f"DELETE FROM afk WHERE gid = '{message.guild.id}' and userid = '{message.author.id}'")
            self.bot.connection.commit()
            await asyncio.sleep(2)
            embed = discord.Embed(
                description="Okay, i see you are back! Welcome back {}! I removed your AFK".format(message.author.mention),
                color=guild_embedcolor_message(self, message))
            embed.set_author(name="AFK System | Welcome back", icon_url=afkicon)
            await message.channel.send(embed=embed, delete_after=10)
            return


def setup(bot):
    bot.add_cog(Afk(bot))
