# import
import asyncio
from io import BytesIO

from Utils.data import *
from discord import emoji
from PIL import ImageDraw, ImageEnhance, Image
from PIL import ImageFont


# class
class Marriage(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def marry(self, ctx, user: discord.User = None):
        if not user:
            embed = discord.Embed(description=f"Uhm, you failed the `target` argument'",
                                  color=guild_embedcolor_ctx(self, ctx))
            await ctx.message.reply(embed=embed, mention_author=False)
        family_id = random.randrange(100000, 999999)
        if user.id == self.bot.user.id:
            embed = discord.Embed(description=f"Hey Sorry, i know you like me, but you can't marry me!'",
                                  color=guild_embedcolor_ctx(self, ctx))
            await ctx.message.reply(embed=embed, mention_author=False)
            return
        if ctx.author.id == user.id:
            embed = discord.Embed(description=f"You can't marry yourself.",
                                  color=guild_embedcolor_ctx(self, ctx))
            await ctx.message.reply(embed=embed, mention_author=False)
            return
        if user.bot:
            embed = discord.Embed(description=f"You can't marry Bots. They would not respond. TvT",
                                  color=guild_embedcolor_ctx(self, ctx))
            await ctx.message.reply(embed=embed, mention_author=False)
            return
        self.bot.cursor.execute(
            f"SELECT targetid FROM marry WHERE targetid = '{user.id}'")
        you = self.bot.cursor.fetchone()
        if you is not None:
            targetname = self.bot.get_user(you[0])
            if targetname is None:
                targetname = await self.bot.fetch_user(you[0])
                embed = discord.Embed(description=f"I'm Sorry, but **{targetname}** is already married",
                                      color=guild_embedcolor_ctx(self, ctx))
                await ctx.message.reply(embed=embed, mention_author=False)
        self.bot.cursor.execute(
            f"SELECT ctxid FROM marry WHERE targetid = '{ctx.author.id}'")
        me = self.bot.cursor.fetchone()
        if me is not None:
            embed = discord.Embed(
                description=f"Hey, {ctx.message.author.mention} you're already married! Divorce your partner first!",
                color=guild_embedcolor_ctx(self, ctx))
            await ctx.message.reply(embed=embed, mention_author=False)
        if me is None and you is not None:
            embed = discord.Embed(
                description=f"Sorry, {ctx.message.author.mention} looks like {user.mention} is already married :pensive:",
                color=guild_embedcolor_ctx(self, ctx))
            await ctx.message.reply(embed=embed, mention_author=False)
        if me is None and you is None:
            embed = discord.Embed(
                description=f"Hey, {ctx.message.author.mention}, it would make {user.mention} very very happy if you marry them. What do you say?\n"
                            f"`Press Yes to Accept`\n"
                            f"`Press No to Decline`",
                color=guild_embedcolor_ctx(self, ctx))
            await ctx.send(embed=embed, view=discord.ui.View(discord.ui.Button(label=f'Yes!', style=discord.ButtonStyle.green, custom_id="yes"), discord.ui.Button(label=f'No!', style=discord.ButtonStyle.red, custom_id="no")))
            try:

                def check_data(message):
                    return message.user == user

                interaction = await self.bot.wait_for('interaction', timeout=30, check=check_data)

                if interaction.data["custom_id"] == "yes":
                    timestampn = datetime.datetime.now().strftime("%d.%m.%Y")
                    sql = ("INSERT INTO marry(ctxid, targetid, timestampm, familyid) VALUES(%s,%s,%s,%s)")
                    val = (str(user.id), (str(ctx.author.id)), timestampn, family_id)
                    self.bot.cursor.execute(sql, val)
                    self.bot.connection.commit()
                    timestampn = datetime.datetime.now().strftime("%d.%m.%Y")
                    sql = ("INSERT INTO marry(ctxid, targetid, timestampm, familyid) VALUES(%s,%s,%s,%s)")
                    val = (str(ctx.author.id), (str(user.id)), timestampn, family_id)
                    self.bot.cursor.execute(sql, val)
                    self.bot.connection.commit()
                    embed = discord.Embed(
                        description=f"Hey, {ctx.message.author.mention} looks like Today is a good day for you! You are now married to {user.mention}.",
                        color=guild_embedcolor_ctx(self, ctx))
                    await interaction.message.reply(embed=embed, mention_author=False)
                    return
                else:
                    embed = discord.Embed(
                        description=f"Sorry, {ctx.message.author.mention}, {user.mention} just said no qwq.",
                        color=guild_embedcolor_ctx(self, ctx))
                    await ctx.message.reply(embed=embed, mention_author=False)
                    return
            except asyncio.TimeoutError:
                embed = discord.Embed(
                    description=f"Sorry, {ctx.message.author.mention}, your request to {user.mention} timed out! they didn't respond in time qwq.",
                    color=guild_embedcolor_ctx(self, ctx))
                await ctx.message.reply(embed=embed, mention_author=False)
                return

    @commands.command()
    async def divorce(self, ctx):
        self.bot.cursor.execute(
            f"SELECT ctxid FROM marry WHERE targetid = '{ctx.author.id}'")
        me = self.bot.cursor.fetchone()
        if me is not None:
            self.bot.cursor.execute(
                f"DELETE FROM marry WHERE ctxid = '{ctx.author.id}'")
            self.bot.connection.commit()
            self.bot.cursor.execute(
                f"DELETE FROM marry WHERE targetid = '{ctx.author.id}'")
            self.bot.connection.commit()
            embed = discord.Embed(
                description=f"Sorry, {ctx.message.author.mention}, i think its a hard decision, but i think its better for you.",
                color=guild_embedcolor_ctx(self, ctx))
            await ctx.message.reply(embed=embed, mention_author=False)
        if me is None:
            embed = discord.Embed(
                description=f"Uhm, {ctx.message.author.mention}, you was not married.",
                color=guild_embedcolor_ctx(self, ctx))
            await ctx.message.reply(embed=embed, mention_author=False)

    @commands.command()
    async def partner(self, ctx, user: discord.User = None):
        if not user:
            self.bot.cursor.execute(
                f"SELECT targetid FROM marry WHERE ctxid = '{ctx.author.id}'")
            me = self.bot.cursor.fetchone()
            if me is None:
                embed = discord.Embed(
                    description=f"Oh, {ctx.author.mention}, looks like you don't have a partner!",
                    color=guild_embedcolor_ctx(self, ctx))
                await ctx.message.reply(embed=embed, mention_author=False)
            if me is not None:
                getpartner = self.bot.get_user(me[0])
                if getpartner is None:
                    getpartner = await self.bot.fetch_user(me[0])
                    pass
                self.bot.cursor.execute(
                    f"SELECT timestampm FROM marry WHERE ctxid = '{ctx.author.id}'")
                timestamp = self.bot.cursor.fetchone()[0]
                embed = discord.Embed(
                    description=f"**{ctx.author}** is married to **{getpartner}** (`{getpartner.id}`). They are married since `{timestamp}`",
                    color=guild_embedcolor_ctx(self, ctx))
                await ctx.message.reply(embed=embed, mention_author=False)
                return
        if user:
            self.bot.cursor.execute(
                f"SELECT targetid FROM marry WHERE ctxid = '{user.id}'")
            me = self.bot.cursor.fetchone()
            if me is None:
                embed = discord.Embed(
                    description=f"Oh, looks like {user.mention} doesn't have a partner!",
                    color=guild_embedcolor_ctx(self, ctx))
                await ctx.message.reply(embed=embed, mention_author=False)
            if me is not None:
                getpartner = self.bot.get_user(me[0])
                if getpartner is None:
                    getpartner = await self.bot.fetch_user(me[0])
                    pass
                self.bot.cursor.execute(
                    f"SELECT timestampm FROM marry WHERE ctxid = '{user.id}'")
                timestamp = self.bot.cursor.fetchone()[0]
                embed = discord.Embed(
                    description=f"**{user}** is married to **{getpartner}** (`{getpartner.id}`). They are married since `{timestamp}`",
                    color=guild_embedcolor_ctx(self, ctx))
                await ctx.message.reply(embed=embed, mention_author=False)
                return


class Profile(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def profile(self, ctx, user: discord.User = None):
        loadmsg = await ctx.send(f"Loading Profile —")
        if not user:
            user = ctx.author
        if user:
            img = Image.open(getbg(self, user))
            enhancer = ImageEnhance.Brightness(img)
            img = enhancer.enhance(0.5)
            draw = ImageDraw.Draw(img)

            await loadmsg.edit(content=f"Loading Profile \\")
            font100 = ImageFont.truetype("Profile/Funtype.ttf", 100)
            font110 = ImageFont.truetype("Profile/Funtype.ttf", 110)
            font80 = ImageFont.truetype("Profile/Funtype.ttf", 80)
            font85 = ImageFont.truetype("Profile/Funtype.ttf", 85)
            font90 = ImageFont.truetype("Profile/Funtype.ttf", 90)
            font75 = ImageFont.truetype("Profile/Funtype.ttf", 75)
            font70 = ImageFont.truetype("Profile/Funtype.ttf", 70)
            font50 = ImageFont.truetype("Profile/Funtype.ttf", 50)
            font55 = ImageFont.truetype("Profile/Funtype.ttf", 55)
            font60 = ImageFont.truetype("Profile/Funtype.ttf", 60)
            font65 = ImageFont.truetype("Profile/Funtype.ttf", 65)
            async with aiohttp.ClientSession() as session:
                async with session.get(str(user.avatar.url)) as response:
                    image = await response.read()

            await loadmsg.edit(content=f"Loading Profile |")
            icon = Image.open(BytesIO(image)).convert("RGBA")
            img.paste(icon.resize((256, 256)), (50, 60))
            draw.text((330, 50), f"{user.name}'s Profile:", (191, 191, 191), font=font110)
            if user.bot:
                draw.text((330, 150), f"BOT ACCOUNT", (255, 0, 0), font=font80)
                pass
            draw.text((25, 330), f"Current Coins:", (37, 205, 247), font=font75)
            draw.text((25, 400), f"{fetchcoins(self, ctx, user)}", (191, 191, 191), font=font70)
            #draw.text((585, 330), f"Current Rank:", (37, 205, 247), font=font75)
            #draw.text((585, 400), f"Level: {fetchrank(self, ctx, user)}, XP: {fetchxp(self, ctx, user)}",
                      #(191, 191, 191), font=font70)
            draw.text((25, 500), f"Current Partner:", (37, 205, 247), font=font75)
            draw.text((25, 570), f"{await getpartner(self, ctx, user)}",
                      (191, 191, 191), font=font70)
            await loadmsg.edit(content=f"Loading Profile /")
            img.save('Profile/tmp.jpg')

            await loadmsg.edit(content=f"Loading Profile —")
            ffile = discord.File("Profile/tmp.jpg")
            await loadmsg.edit(content=f"Loading Profile \\")
            await asyncio.sleep(0.1)
            await loadmsg.edit(content=f"Loading Profile |")
            await loadmsg.edit(content=f"Profile Loaded.. Sending!")
            await asyncio.sleep(0.1)
            await loadmsg.delete()
            await ctx.send(file=ffile)


def getbg(self, user):
    cursor = self.bot.connection.cursor()
    cursor.execute(
        f"SELECT index FROM userbg WHERE user_id = '{user.id}'")
    bg = cursor.fetchone()
    if bg is None:
        return "Profile/profilecard1.jpg"
    if bg is not None:
        cursor = self.bot.connection.cursor()
        cursor.execute(
            f"SELECT path FROM backgrounddb WHERE user_id = '{user.id}'")
        bg = cursor.fetchone()
        return f"{bg}"

async def getpartner(self, ctx, user):
    if not user:
        user = ctx.author
    if user:
        self.bot.cursor.execute(
            f"SELECT targetid FROM marry WHERE ctxid = '{user.id}'")
        me = self.bot.cursor.fetchone()
        if me is None:
            return "Not married"
        if me is not None:
            fetchpartner = self.bot.get_user(me[0])
            if fetchpartner is None:
                fetchpartner = await self.bot.fetch_user(me[0])
                pass
            return fetchpartner

def fetchxp(self, ctx, user):
    if not user:
        user = ctx.author
    if user:
        cursor = self.bot.connection.cursor()
        cursor.execute(
            f"SELECT exp FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{user.id}'")
        current_rank = cursor.fetchone()
        if current_rank is None:
            return 0
        if current_rank is not None:
            return current_rank[0]


def fetchrank(self, ctx, user):
    if not user:
        user = ctx.author
    if user:
        cursor = self.bot.connection.cursor()
        cursor.execute(
            f"SELECT level FROM glevel WHERE guild_id = '{ctx.guild.id}' and user_id = '{user.id}'")
        current_rank = cursor.fetchone()
        if current_rank is None:
            return 0
        if current_rank is not None:
            return current_rank[0]


def fetchcoins(self, ctx, user):
    if not user:
        user.id = ctx.author.id
    if user:
        cursor = self.bot.connection.cursor()
        cursor.execute(
            f"SELECT coins FROM currency WHERE user_id = {int(user.id)} AND guild_id = {ctx.guild.id}")
        current_coins = cursor.fetchone()
        if current_coins is None:
            return "0 - Not Used"
        if current_coins is not None:
            return current_coins[0]


def setup(bot):
    bot.add_cog(Marriage(bot))
    bot.add_cog(Profile(bot))
