import discord.ext.commands

from Utils.data import *

stupidword = "https://cdn.discordapp.com/attachments/836905275252408341/838075043271016468/StupidWord.png"

DISCORD_INVITE = r'discord(?:app\.com|\.gg)[\/invite\/]?(?:(?!.*[Ii10OolL]).[a-zA-Z0-9]{5,7}|[a-zA-Z0-9\-]{2,32})'


class ImageOnlyAutomod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def imageonly(self, ctx):
        embed = discord.Embed(
            description=f'**AutoModeration Image-Only Channel**\n\n> `{prefix_data(ctx.guild.id)}imageonly add` Adds a new Channel\n> `{prefix_data(ctx.guild.id)}imageonly remove` Removes a Channel\n> `{prefix_data(ctx.guild.id)}imageonly list` List all Channels\n> `{prefix_data(ctx.guild.id)}imageonly clear` Clears all configured Channels!',
            color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name="Automoderation | Image-Only",
                         icon_url="https://cdn.discordapp.com/attachments/836905275252408341/837266055709589504/StupidImage2.png")
        await ctx.message.reply(embed=embed, mention_author=False)

    @imageonly.command(aliases=["set"])
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, channelid: discord.TextChannel = None):
        try:
            channelid = channelid.id
        except AttributeError:
            pass
        try:
            if not channelid:
                embed = discord.Embed(description="You need to mention the Channel or its ID",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="No Channel given", icon_url=cross_icon())
                await ctx.send(embed=embed)
                return
        except AttributeError:
            return
        self.bot.cursor.execute(
            f"SELECT channelid FROM imageonly WHERE guildid = '{ctx.guild.id}' and channelid = '{channelid}'")
        result = self.bot.cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO imageonly(guildid, channelid) VALUES(%s,%s)")
            val = (str(ctx.guild.id), channelid)
            self.bot.cursor.execute(sql, val)
            self.bot.connection.commit()
            embed = discord.Embed(description=f"Channel <#{channelid}> added to the Image-Only Automoderation")
            embed.set_author(name="Automoderation | Image-Only", icon_url=chop_icon())
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description=f"Channel <#{channelid}> is already added!",
                                  color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Image-Only", icon_url=cross_icon())
            await ctx.message.reply(embed=embed, mention_author=False)

    @imageonly.command(aliases=["unset"])
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, channelid: discord.TextChannel = None):
        try:
            channelid = channelid.id
        except AttributeError:
            pass
        try:
            if not channelid:
                embed = discord.Embed(description="You need to mention the Channel or its ID",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="No Channel given", icon_url=cross_icon())
                await ctx.send(embed=embed)
                return
        except AttributeError:
            return
        self.bot.cursor.execute(
            f"SELECT channelid FROM imageonly WHERE guildid = '{ctx.guild.id}' and channelid = '{channelid}'")
        result = self.bot.cursor.fetchone()
        if result is not None:
            self.bot.cursor.execute(
                "DELETE FROM imageonly WHERE guildid = '{}' and channelid = '{}'".format(ctx.guild.id, channelid))
            self.bot.connection.commit()
            embed = discord.Embed(description=f"Channel <#{channelid}> removed", color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Image-Only", icon_url=chop_icon())
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description=f"Channel <#{channelid}> not set as Image-Only!",
                                  color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Image-Only", icon_url=cross_icon())
            await ctx.message.reply(embed=embed, mention_author=False)

    @imageonly.command(name='list')
    @commands.has_permissions(administrator=True)
    async def _list(self, ctx):
        self.bot.cursor.execute(f"SELECT channelid FROM imageonly WHERE guildid = '{ctx.guild.id}'")
        result = self.bot.cursor.fetchall()
        res = list()
        for i in result:
            res.append(str(i[0]))
        if res == []:

            embed = discord.Embed(description="No Entrys", color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Image-Only", icon_url=cross_icon())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=", ".join(res), color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Image-Only", icon_url=cross_icon())
            await ctx.send(embed=embed)

    @imageonly.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx):
        self.bot.cursor.execute(f"DELETE FROM imageonly WHERE guildid = '{ctx.guild.id}'")
        self.bot.connection.commit()
        embed = discord.Embed(description=f"Removed all Channels from Database.", color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name="Automoderation | Image-Only", icon_url=chop_icon())
        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.guild:
                self.bot.cursor.execute(
                    f"SELECT channelid FROM imageonly WHERE channelid = {message.channel.id} AND guildid = {message.guild.id}")
                result = self.bot.cursor.fetchone()[0]
                if message.channel.id == result:
                    if result is not None:
                        if message.attachments == []:
                            await message.delete()
                            try:
                                embed = discord.Embed(
                                    description=f"Hey, `{message.author.name}`, the `{message.channel.name}` channel on `{message.guild.name}` is only for images. Please avoid sending text messages and instead send images only.",
                                    color=color_data())
                                embed.set_author(name=f"Image Only Channel!",
                                                 icon_url="https://cdn.discordapp.com/attachments/771085429381922856/835885280367476796/2915_denied.png")
                                await message.author.send(embed=embed)
                            except AttributeError:
                                pass
                            except discord.errors.NotFound:
                                pass
        except TypeError:
            pass


class BadWordAutomod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.group(invoke_without_command=True)
    async def badword(self, ctx):
        embed = discord.Embed(
            description=f'**AutoModeration Badword List**\n\n> `{prefix_data(ctx.guild.id)}badword add` Adds a new Word\n> `{prefix_data(ctx.guild.id)}badword remove` Removes a Word\n> `{prefix_data(ctx.guild.id)}badword list` List all Badwords\n>  `{prefix_data(ctx.guild.id)}badword clear` Clears all configured Badwords!',
            color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name="Automoderation | Badword",
                         icon_url=stupidword)
        embed.set_footer(
            text="Administrators are immune upon deletion! Added badwords only work if set lowercase! Dont worry it will Moderated if not lowercase in chat!")
        await ctx.message.reply(embed=embed, mention_author=False)

    @badword.command()
    @commands.has_permissions(administrator=True)
    async def add(self, ctx, badword):
        try:
            if not badword:
                embed = discord.Embed(description="You Need to say the badword that should be added in to the database",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="No Word given", icon_url=cross_icon())
                await ctx.send(embed=embed)
                return
        except AttributeError:
            return
        self.bot.cursor.execute(
            f"SELECT word FROM badword WHERE guildid = '{ctx.guild.id}' AND word = '{badword}'")
        result = self.bot.cursor.fetchone()
        if result is None:
            sql = ("INSERT INTO badword(guildid, word) VALUES(%s,%s)")
            val = (str(ctx.guild.id), badword)
            self.bot.cursor.execute(sql, val)
            self.bot.connection.commit()
            embed = discord.Embed(description=f"Word: `{badword}` added to the Automoderation Database",
                                  color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Badword", icon_url=chop_icon())
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description=f"Word: `{badword}` is already added!",
                                  color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Badword", icon_url=cross_icon())
            await ctx.message.reply(embed=embed, mention_author=False)

    @badword.command()
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, badword):
        try:
            if not badword:
                embed = discord.Embed(description="You Need to say the badword that should be added in to the database",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="No Word given", icon_url=cross_icon())
                await ctx.send(embed=embed)
                return
        except AttributeError:
            return
        self.bot.cursor.execute(
            f"SELECT word FROM badword WHERE guildid = '{ctx.guild.id}' AND word = '{badword}'")
        result = self.bot.cursor.fetchone()
        if result is not None:
            self.bot.cursor.execute(
                "DELETE FROM badword WHERE guildid = '{}' and word = '{}'".format(ctx.guild.id, badword))
            self.bot.connection.commit()
            embed = discord.Embed(description=f"Word: `{badword}` removed", color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Badword", icon_url=chop_icon())
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(description="Word: `{}` not set as Badword!".format(badword),
                                  color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Badword", icon_url=cross_icon())
            await ctx.message.reply(embed=embed, mention_author=False)

    @badword.command(name='list')
    @commands.has_permissions(administrator=True)
    async def _list(self, ctx):
        self.bot.cursor.execute(f"SELECT word FROM badword WHERE guildid = '{ctx.guild.id}'")
        result = self.bot.cursor.fetchall()
        res = list()
        for i in result:
            res.append(str(i[0]))
        if res == []:

            embed = discord.Embed(description="No Entrys", color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Badword", icon_url=cross_icon())
            await ctx.send(embed=embed)

        else:
            embed = discord.Embed(description=", ".join(res), color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Automoderation | Badword", icon_url=cross_icon())
            await ctx.send(embed=embed)

    @badword.command()
    @commands.has_permissions(administrator=True)
    async def clear(self, ctx):
        self.bot.cursor.execute(f"DELETE FROM badword WHERE guildid = '{ctx.guild.id}'")
        self.bot.connection.commit()
        embed = discord.Embed(description=f"Removed all Badwords from Database.", color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name="Automoderation | Badword", icon_url=chop_icon())
        await ctx.message.reply(embed=embed, mention_author=False)

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            if message.guild:
                self.bot.cursor.execute(
                    f"SELECT word FROM badword WHERE guildid = '{message.guild.id}'")
                result = self.bot.cursor.fetchall()
                result2 = [i[0] for i in result]
                if any(word in message.content.lower() for word in result2):
                    if message.author.guild_permissions.administrator: return
                    if not discord.utils.get(message.author.roles, id=771734897475059753) in message.author.roles:
                        await message.delete()
                        try:
                            embed = discord.Embed(
                                description=f"Hey, `{message.author.name}`, please try to avoid sending blacklisted words on `{message.guild.name}`",
                                color=guild_embedcolor_message(self, message))
                            embed.set_author(name="Bad Word!", icon_url=stupidword)
                            await message.author.send(embed=embed)
                        except AttributeError:
                            pass
        except TypeError:
            pass


class GenAutomod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            timestampinv = datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S")
            try:
                self.bot.cursor.execute(
                    f"SELECT gid FROM antiinvite WHERE gid = '{message.guild.id}'")
                setting = self.bot.cursor.fetchone()
                if setting is not None:
                    regex = re.compile(DISCORD_INVITE)
                    invites = regex.findall(message.content)
                    if invites:
                        if message.author.guild_permissions.administrator: return
                        if message.author.bot: return
                        invite = invites[0]
                        invitedb = invites[0]
                        invite = await self.bot.fetch_invite(invite)
                        if invite.guild.id == message.guild.id: return
                        try:
                            self.bot.cursor.execute(f"DELETE FROM invitedb WHERE guildid = '{message.guild.id}'")
                            self.bot.connection.commit()
                        except:
                            pass
                        sql = ("INSERT INTO invitedb(guildid, inviteurl, invts, uname) VALUES(%s,%s,%s,%s)")
                        val = (str(message.guild.id), invitedb, timestampinv, str(message.author))
                        self.bot.cursor.execute(sql, val)
                        self.bot.connection.commit()
                        await message.delete()
                        embed = discord.Embed(
                            description="Hey {}, don't send invites! Server Invites are not allowed here!".format(
                                message.author.mention), color=guild_embedcolor_message(self, message))
                        embed.set_author(name=f"Auto-Mod | Anti-Invite | Invite Posted!",
                                         icon_url="https://cdn.discordapp.com/attachments/836905275252408341/837285292377243679/Error-512.png")
                        await message.channel.send(embed=embed)
                        try:
                            embed = discord.Embed(
                                description=f"Hey, `{message.author.name}`, don't send invites on `{message.guild.name}`! Thats forbidden!",
                                color=color_data())
                            embed.set_author(name=f"Auto-Mod | Anti-Invite | Invite Posted!",
                                             icon_url="https://cdn.discordapp.com/attachments/836905275252408341/837285292377243679/Error-512.png")
                            await message.author.send(embed=embed)
                        except AttributeError:
                            pass
            except AttributeError:
                pass
        except:
            self.bot.connection.rollback()

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def lastinvite(self, ctx, gid: discord.Guild = None):
        if not gid:
            gid = ctx.guild
        try:
            g = self.bot.get_guild(gid.id)
            self.bot.cursor.execute(f"SELECT inviteurl FROM invitedb WHERE guildid = '{gid.id}'")
            result = self.bot.cursor.fetchone()[0]
            self.bot.cursor.execute(f"SELECT invts FROM invitedb WHERE guildid = '{gid.id}'")
            resultts = self.bot.cursor.fetchone()[0]
            self.bot.cursor.execute(f"SELECT uname FROM invitedb WHERE guildid = '{gid.id}'")
            rname = self.bot.cursor.fetchone()[0]
            await ctx.send(result)
            await ctx.send("Last Invite from {}, it was sent {}, the User was {}".format(g.name, resultts, rname))
        except:
            g = self.bot.get_guild(gid.id)
            embed = discord.Embed(description="No Invite was posted in {}!".format(g.name),
                                  color=guild_embedcolor_ctx(self, ctx))
            await ctx.message.reply(embed=embed, mention_author=False)
            return

    @commands.has_permissions(administrator=True)
    @commands.command()
    async def clearlastinvite(self, ctx):
        try:
            self.bot.cursor.execute(f"DELETE FROM invitedb WHERE guildid = '{ctx.guild.id}'")
            self.bot.connection.commit()
        except:
            pass
        embed = discord.Embed(description="Invite Cache was cleared!", color=guild_embedcolor_ctx(self, ctx))
        await ctx.message.reply(embed=embed, mention_author=False)


    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def antiinvite(self, ctx, state=None):
        if state:
            if state == "on" or state == "enable":
                self.bot.cursor.execute(
                    f"SELECT gid FROM antiinvite WHERE gid = '{ctx.guild.id}'")
                setting = self.bot.cursor.fetchone()
                if setting is None:
                    sql = ("INSERT INTO antiinvite(gid, index) VALUES(%s,%s)")
                    val = (str(ctx.guild.id), "1")
                    self.bot.cursor.execute(sql, val)
                    self.bot.connection.commit()
                    embed = discord.Embed(description=f"Anti-Invite is now `Enabled`",
                                          color=guild_embedcolor_ctx(self, ctx))
                    await ctx.message.reply(embed=embed, mention_author=False)
                    return
                if setting is not None:
                    embed = discord.Embed(
                        description=f"Anti-Invite was already `Enabled`, to disable it type {prefix_data(ctx.guild.id)}disable",
                        color=guild_embedcolor_ctx(self, ctx))
                    await ctx.message.reply(embed=embed, mention_author=False)
                    return
            if state == "off" or state == "disable":
                self.bot.cursor.execute(
                    f"SELECT gid FROM antiinvite WHERE gid = '{ctx.guild.id}'")
                setting = self.bot.cursor.fetchone()
                if setting is not None:
                    self.bot.cursor.execute(f"DELETE FROM antiinvite WHERE gid = '{ctx.guild.id}'")
                    self.bot.connection.commit()
                    embed = discord.Embed(description=f"Anti-Invite is now `Disabled`",
                                          color=guild_embedcolor_ctx(self, ctx))
                    await ctx.message.reply(embed=embed, mention_author=False)
                    return
                if setting is None:
                    embed = discord.Embed(
                        description=f"Anti-Invite was already `disabled`, to enable it type {prefix_data(ctx.guild.id)}enable",
                        color=guild_embedcolor_ctx(self, ctx))
                    await ctx.message.reply(embed=embed, mention_author=False)
                    return
        if not state:
            self.bot.cursor.execute(
                f"SELECT gid FROM antiinvite WHERE gid = '{ctx.guild.id}'")
            setting = self.bot.cursor.fetchone()
            if setting is None:
                embed = discord.Embed(description=f"Anti-Invite is `Disabled`",
                                      color=guild_embedcolor_ctx(self, ctx))
                await ctx.message.reply(embed=embed, mention_author=False)
                return
            if setting is not None:
                embed = discord.Embed(description=f"Anti-Invite is `Enabled`",
                                      color=guild_embedcolor_ctx(self, ctx))
                await ctx.message.reply(embed=embed, mention_author=False)
                return


def setup(bot):
    bot.add_cog(ImageOnlyAutomod(bot))
    bot.add_cog(BadWordAutomod(bot))
    bot.add_cog(GenAutomod(bot))
