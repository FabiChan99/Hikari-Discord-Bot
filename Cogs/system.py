# import
import discord
import dbl
import statcord
from Utils.data import *

setting_icon = "https://cdn.discordapp.com/attachments/836905275252408341/838442346345005096/StupidSettings.png"
warning_icon = "https://cdn.discordapp.com/attachments/836905275252408341/837285292377243679/Error-512.png"
color_icon = "https://cdn.discordapp.com/attachments/836905275252408341/838468027787509760/StupidColor.png"



de_flag = "\U0001f1e9\U0001f1ea"
us_flag = "\U0001f1fa\U0001f1f8"
jp_flag = "\U0001f1ef\U0001f1f5"

def cmdstats(self, ctx):
    self.bot.cursor.execute(
        f"SELECT cnt FROM cmdstats WHERE cmd = '{ctx.command.name}'")
    result = self.bot.cursor.fetchone()
    if result is None:
        sql = ("INSERT INTO cmdstats(cmd, cnt) VALUES(%s,%s)")
        val = ((str(ctx.command.name)), "1")
        self.bot.cursor.execute(sql, val)
        self.bot.connection.commit()
    if result is not None:
        self.bot.cursor.execute(
            f"SELECT cnt FROM cmdstats WHERE cmd = '{ctx.command.name}'")
        result = self.bot.cursor.fetchone()[0]
        resultnew = result + 1
        self.bot.cursor.execute(
            f"DELETE FROM cmdstats WHERE cmd = '{ctx.command.name}'")
        self.bot.connection.commit()
        sql = ("INSERT INTO cmdstats(cmd, cnt) VALUES(%s,%s)")
        val = ((str(ctx.command.name)), resultnew)
        self.bot.cursor.execute(sql, val)
        self.bot.connection.commit()

# class
class System(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot



    @commands.Cog.listener()
    async def on_command(self, ctx):
        setup_guild(ctx.guild)
        cmdstats(self, ctx)



#    @commands.command(aliases=['startyoutube'])
#    async def startyt(self, ctx):
#
#        link = await self.together.create_link(ctx.author.voice.channel.id, 'youtube')
#        embed = discord.Embed(description=f'[Click here]({link}) to start YouTube or use the link that was sent .',
#                              color=0x5865F2)
#        embed.set_author(name='Here is your activity link',
#                         icon_url='https://cdn.discordapp.com/emojis/828650661972672623.png?v=1')
#        embed.set_footer(text='If the link is invalid check if the bot has permissions to the voice channel')
#        await ctx.send(embed=embed,
#                                  content=link)
#        #except:
#            #embed = discord.Embed(description="You need in a Voice Channel to use this feature",
#            #                      color=guild_embedcolor_ctx(self, ctx))
#            #await ctx.send(embed=embed)


    # prefix
    @commands.has_permissions(manage_channels=True)
    @commands.command()
    async def prefix(self, ctx, *, new_prefix=None):
        if new_prefix:
            guild = prefix_db.find_one({"_id": int(ctx.guild.id)})
            if guild['prefix'] == new_prefix:
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"The prefix is already {new_prefix}")
                embed.add_field(name=f'> Note:',
                                value=f'You can also use **{self.bot.user.mention} help** to use the bot')
                await ctx.message.reply(embed=embed, mention_author=False)
                return
            else:
                prefix_db.update_one({"_id": int(ctx.guild.id)}, {"$set": {"prefix": str(new_prefix)}})
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"The prefix has been changed to {new_prefix}")
                embed.add_field(name=f'> Note:',
                                value=f'You can also use **{self.bot.user.mention} help** to use the bot')
                await ctx.message.reply(embed=embed, mention_author=False)
                return
        else:
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"The new prefix is missing!")
            embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}prefix [new_prefix]')
            await ctx.message.reply(embed=embed, mention_author=False)
            return

    # supportserver
    @commands.command()
    async def support(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Support server", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'You can join the support server here', value=f'https://discord.gg/XpPnY9NRwf',
                        inline=False)
        embed.set_footer(text=f'Join here for Support ;)')
        await ctx.message.reply(embed=embed, mention_author=False)
        return



    # vote
    @commands.command()
    async def vote(self, ctx):
        agc = self.bot.get_emoji(910176042143080479)
        hikari = self.bot.get_emoji(910176055342530600)
        if ctx.guild.id == 750365461945778209:
            embed = discord.Embed(description=f"Vote für uns in dem du auf den untenstehenden Link klickst. <:AGC_PepCuteHeart:842393744284057600>", color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(text=f"Vielen Dank fürs Voten , Damit leistest du uns Unterstützung ")
            embed.set_author(name="Voting", icon_url="https://cdn.discordapp.com/emojis/825695714620211220.png?size=44")
            await ctx.send(embed=embed, view=discord.ui.View(discord.ui.Button(label=f'Vote für Anime & Gaming Café', style=discord.ButtonStyle.grey, emoji=agc, url="https://top.gg/servers/750365461945778209/vote"), discord.ui.Button(label=f'Vote für Hikari', style=discord.ButtonStyle.grey, emoji=hikari, url="https://top.gg/bot/811742311692238860/vote")))
        else:
            embed = discord.Embed(description="Voting helps a lot, we really appreciate it <:HikariHeart:825695714620211220>", color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Voting", icon_url="https://cdn.discordapp.com/emojis/825695714620211220.png?size=44")
            await ctx.message.reply(embed=embed, mention_author=False, view=discord.ui.View(discord.ui.Button(label=f'Vote for Hikari', style=discord.ButtonStyle.grey, emoji=hikari, url="https://top.gg/bot/811742311692238860/vote")))

    # inviteme

    @commands.command(aliases=['invite'])
    async def botinvite(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.add_field(name=f'My Invite Link:',
                        value=f'[Invite Hikari](https://discord.com/oauth2/authorize?client_id={self.bot.user.id}&permissions=1073217527&scope=applications.commands%20bot) <:HikariHeart:825695714620211220>',
                        inline=False)
        embed.set_footer(text=f'Click at the Link to invite me!')
        await ctx.message.reply(embed=embed, mention_author=False)
        return


class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        try:
            self.bot.cursor.execute(
                f"SELECT guildid FROM reactonmention WHERE guildid = '{message.guild.id}'")
        except:
            pass
        try:
            result = self.bot.cursor.fetchone()
            if result is not None:
                if self.bot.user.mentioned_in(message) and message.mention_everyone is False:
                    await message.add_reaction('<:HikariHeart:825695714620211220>')
        except:
            pass

    @commands.command(aliases=["rop"])
    @commands.has_permissions(administrator=True)
    async def reactonping(self, ctx, setting=None):
        if not setting:
            self.bot.cursor.execute(
                f"SELECT guildid FROM reactonmention WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result == None:
                embed = discord.Embed(
                    description=f"React with <:HikariHeart:825695714620211220> on Ping is currently `Disabled`! Enable it with `{prefix_data(ctx.guild.id)}reactonping enable`",
                    color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="Settings | React on Ping", icon_url=setting_icon)
                await ctx.message.reply(embed=embed, mention_author=False)
            if result is not None:
                embed = discord.Embed(
                    description=f"React with <:HikariHeart:825695714620211220> on Ping is currently `Enabled`! Disable it with `{prefix_data(ctx.guild.id)}reactonping disable`",
                    color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="Settings | React on Ping", icon_url=setting_icon)
                await ctx.message.reply(embed=embed, mention_author=False)
        if setting == "enable" or setting == "on":
            self.bot.cursor.execute(
                f"SELECT guildid FROM reactonmention WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is not None:
                embed = discord.Embed(
                    description=f"React with <:HikariHeart:825695714620211220> on Ping is already `Enabled`! Disable it with `{prefix_data(ctx.guild.id)}reactonping disable`",
                    color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="Settings | React on Ping", icon_url=warning_icon)
                await ctx.message.reply(embed=embed, mention_author=False)
                return
            sql = ("INSERT INTO reactonmention(guildid, setting) VALUES(%s,%s)")
            val = (str(ctx.guild.id), "enabled")
            try:
                self.bot.cursor.execute(sql, val)
                self.bot.connection.commit()
            except:
                self.bot.connection.rollback()
            embed = discord.Embed(
                description=f"React with <:HikariHeart:825695714620211220> on Ping is now `Enabled`! Disable it with `{prefix_data(ctx.guild.id)}reactonping disable`",
                color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="Settings | React on Ping", icon_url=chop_icon())
            await ctx.message.reply(embed=embed, mention_author=False)
            return
        if setting == "disable" or setting == "off":
            self.bot.cursor.execute(
                f"SELECT guildid FROM reactonmention WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                embed = discord.Embed(
                    description=f"React with <:HikariHeart:825695714620211220> on Ping is already `Disabled`! Enable it with `{prefix_data(ctx.guild.id)}reactonping enable`",
                    color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="Settings | React on Ping", icon_url=warning_icon)
                await ctx.message.reply(embed=embed, mention_author=False)
                return
            if result is not None:
                self.bot.cursor.execute(
                    f"DELETE FROM reactonmention WHERE guildid = '{ctx.guild.id}'")
                self.bot.connection.commit()
                embed = discord.Embed(
                    description=f"React with <:HikariHeart:825695714620211220> on Ping is now `Disabled`! Enable it with `{prefix_data(ctx.guild.id)}reactonping enable`",
                    color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="Settings | React on Ping", icon_url=chop_icon())
                await ctx.message.reply(embed=embed, mention_author=False)
                return



class SettingsEmbed(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def embedcolor(self, ctx, color=None):
        if color == "default" or color == "clear" or color == "reset":
            self.bot.cursor.execute(
                f"SELECT color FROM embedcolor WHERE gid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is not None:
                self.bot.cursor.execute(
                    f"DELETE FROM embedcolor WHERE gid = '{ctx.guild.id}'")
                self.bot.connection.commit()
                embed = discord.Embed(description=f"The Embed color is now set to `Default`",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"Settings | Embed-Color", icon_url=chop_icon())
                await ctx.message.reply(embed=embed, mention_author=False)
                return
            if result is None:
                embed = discord.Embed(description=f"The Embed color was not set, so its already `Default`",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"Settings | Embed-Color", icon_url=chop_icon())
        if not color:
            self.bot.cursor.execute(
                f"SELECT color FROM embedcolor WHERE gid = '{ctx.guild.id}'")
            try:
                result = self.bot.cursor.fetchone()[0]
            except Exception:
                result = None
            if result is not None:
                embed = discord.Embed(description=f"The Current colorcode is: `{result}`",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"Settings | Embed-Color", icon_url=color_icon)
                await ctx.send(embed=embed)
                return
            if result is None:
                embed = discord.Embed(description=f"The Current colorcode is: `Default`",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"Settings | Embed-Color", icon_url=color_icon)
                await ctx.send(embed=embed)
                return
        match = re.search(r'^(?:[0-9a-fA-F]{3}){1,2}$', color)
        if not match:
            embed = discord.Embed(description=f"The Code `{color}` is not a valid hexcode! Example:`00BFFF`\n"
                                              f"Hexcode Range: `000000` - `FFFFFF`\n"
                                              f"**Note**: If your hexcode starts with a # it will not be recognized as one.",
                                  color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"Settings | Embed-Color", icon_url=chop_icon())
            await ctx.message.reply(embed=embed, mention_author=False)
            return
        if color:
            self.bot.cursor.execute(
                f"SELECT gid FROM embedcolor WHERE gid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                sql = ("INSERT INTO embedcolor(gid, color) VALUES(%s,%s)")
                val = (str(ctx.guild.id), color)
                self.bot.cursor.execute(sql, val)
                self.bot.connection.commit()
                embed = discord.Embed(description=f"The New colorcode is: `{color}`",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"Settings | Embed-Color", icon_url=color_icon)
                await ctx.send(embed=embed)
                return
            if result:
                self.bot.cursor.execute(
                    f"DELETE FROM embedcolor WHERE gid = '{ctx.guild.id}'")
                self.bot.connection.commit()
                sql = ("INSERT INTO embedcolor(gid, color) VALUES(%s,%s)")
                val = (str(ctx.guild.id), color)
                self.bot.cursor.execute(sql, val)
                self.bot.connection.commit()
                embed = discord.Embed(description=f"The New colorcode is: `{color}`",
                                      color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"Settings | Embed-Color", icon_url=color_icon)
                await ctx.send(embed=embed)
                return





def setup(bot):
    bot.add_cog(System(bot))
    bot.add_cog(Settings(bot))
    bot.add_cog(SettingsEmbed(bot))
