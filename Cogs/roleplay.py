# import
from Utils.data import *

def rp_ct(self, ctx):
    self.bot.cursor.execute(
        f"SELECT counter FROM roleplayct WHERE userid = '{ctx.author.id}' and cmd = '{ctx.command.name}'")
    result = self.bot.cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO roleplayct(userid, cmd, counter) VALUES(%s,%s,%s)")
        val = (str(ctx.author.id), (str(ctx.command.name)), "1")
        self.bot.cursor.execute(sql, val)
        self.bot.connection.commit()
        result = 0
    if result is not None:
        self.bot.cursor.execute(
            f"SELECT counter FROM roleplayct WHERE userid = '{ctx.author.id}' and cmd = '{ctx.command.name}'")
        result = self.bot.cursor.fetchone()[0]
        resultnew = result + 1
        self.bot.cursor.execute(
            f"UPDATE roleplayct SET counter = {resultnew} WHERE userid = '{ctx.author.id}' and cmd = '{ctx.command.name}'")
        self.bot.connection.commit()
    rpdb = result
    return rpdb

def urp_ct(self, ctx, user):
    self.bot.cursor.execute(
        f"SELECT counter FROM uroleplayct WHERE userid = '{ctx.author.id}' and cmd = '{ctx.command.name}' and targetid = '{user.id}'")
    result = self.bot.cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO uroleplayct(userid, targetid, cmd, counter) VALUES(%s,%s,%s,%s)")
        val = (str(ctx.author.id), (str(user.id)), (str(ctx.command.name)), "1")
        self.bot.cursor.execute(sql, val)
        self.bot.connection.commit()
        result = 0
    if result is not None:
        self.bot.cursor.execute(
            f"SELECT counter FROM uroleplayct WHERE userid = '{ctx.author.id}' and cmd = '{ctx.command.name}' and targetid = '{user.id}'")
        result = self.bot.cursor.fetchone()[0]
        resultnew = result + 1
        self.bot.cursor.execute(
            f"UPDATE uroleplayct SET counter = {resultnew} WHERE userid = '{ctx.author.id}' and cmd = '{ctx.command.name}' and targetid = '{user.id}'")
        self.bot.connection.commit()
    urpdb = result
    return urpdb


class Roleplay(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot




    # kiss
    @commands.command()
    async def kiss(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} kissed {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You kissed {user.name} {urp_ct(self, ctx, user)} times and kissed globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} kissed someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You kissed other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)

        await ctx.send(embed=embed, mention_author=False)


    # bite
    @commands.command()
    async def bite(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} bit {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You bit {user.name} {urp_ct(self, ctx, user)} times and bit globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} bit someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You bit other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)

        await ctx.send(embed=embed, mention_author=False)

    # cry
    @commands.command()
    async def cry(self, ctx, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        embed = discord.Embed(title=f'{ctx.author.name} cried', color=guild_embedcolor_ctx(self, ctx))
        embed.set_footer(text=f"{ctx.author} | You cried {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # cuddle
    @commands.command()
    async def cuddle(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} cuddled {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You cuddled {user.name} {urp_ct(self, ctx, user)} times and cuddled globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} cuddled someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You cuddled other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # slap
    @commands.command()
    async def slap(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} slapped {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You slapped {user.name} {urp_ct(self, ctx, user)} times and slapped globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} slapped someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You slapped other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # punch
    @commands.command()
    async def punch(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} punched {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You punched {user.name} {urp_ct(self, ctx, user)} times and punched globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} punched someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You punched other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # blush
    @commands.command()
    async def blush(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} blushed at {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You blushed at {user.name} {urp_ct(self, ctx, user)} times and blushed globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} blushed', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You blushed at other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # sip
    @commands.command()
    async def sip(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://api.hikaribot.me:6969/sip") as r:
                image = await r.text()

            embed = discord.Embed(title=f'{ctx.author.name} sips', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You sipped {rp_ct(self, ctx)} times in total")
            if msg:
                embed.add_field(name="\u200b", value="> {}".format(msg))
            embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # wave
    @commands.command()
    async def wave(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} waved at {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You waved at {user.name} {urp_ct(self, ctx, user)} times and waved globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} waved', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You waved at other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # love
    @commands.command()
    async def love(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} loves {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You loved {user.name} {urp_ct(self, ctx, user)} times and spreaded love globally {rp_ct(self, ctx)} times")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} loves someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You loved other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # pat
    @commands.command()
    async def pat(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} patted {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You patted {user.name} {urp_ct(self, ctx, user)} times and patted globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} patted someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You patted other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # lick
    @commands.command()
    async def lick(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} licked {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You licked {user.name} {urp_ct(self, ctx, user)} times and licked globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} licked someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You licked other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # hug
    @commands.command()
    async def hug(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} hugged {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You hugged {user.name} {urp_ct(self, ctx, user)} times and hugged globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} hugged someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You hugged other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # poke
    @commands.command()
    async def poke(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} poked {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You poked {user.name} {urp_ct(self, ctx, user)} times and poked globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} poked someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You poked other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)

    # kill
    @commands.command()
    async def kill(self, ctx, user: discord.User = None, *, msg = None):
        async with aiohttp.ClientSession() as session:
            async with session.get(getapiurl(ctx)) as r:
                image = await r.text()
        if user:
            embed = discord.Embed(title=f'{ctx.author.name} killed {user.name}', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You killed {user.name} {urp_ct(self, ctx, user)} times and killed globally {rp_ct(self, ctx)} times in total")
        else:
            embed = discord.Embed(title=f'{ctx.author.name} killed someone', color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"{ctx.author} | You killed other Users {rp_ct(self, ctx)} times in total")
        if msg:
            embed.add_field(name="\u200b", value="> {}".format(msg))
        embed.set_image(url=image)
        await ctx.send(embed=embed, mention_author=False)





def setup(bot):
    bot.add_cog(Roleplay(bot))
