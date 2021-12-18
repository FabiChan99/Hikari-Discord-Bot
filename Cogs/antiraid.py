import discord

from Utils.data import *


# class
class AntiRaid(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        try:
            # antijoin
            self.bot.cursor.execute(
                f"SELECT index FROM antijoin WHERE guildid = '{member.guild.id}'")
            antijoin = self.bot.cursor.fetchone()
            if antijoin is not None:
                embed = discord.Embed(description=f"This Server has enabled an Anti-Join mode, so you can't enter this Server until it get disabled! It's enabled because this Server probably get Raided", color=guild_embedcolor_member(self, member))
                embed.set_author(name="AntiRaid | SafeMode")
                await member.send(embed=embed)
                self.bot.cursor.execute(
                    f"SELECT index FROM raidsafemode WHERE guildid = '{member.guild.id}'")
                safemode = self.bot.cursor.fetchone()
                if safemode is not None:
                    await member.ban(reason="Anit-Join is Enabled! | Safemode is set to High")
                if safemode is None:
                    await member.kick(reason="Anit-Join is Enabled!")
            # picturecheck
            self.bot.cursor.execute(
                f"SELECT index FROM picturecheck WHERE guildid = '{member.guild.id}'")
            piccheck = self.bot.cursor.fetchone()
            if piccheck is not None:
                if not member.avatar:
                    embed = discord.Embed(
                        description=f"Your account has been classified as suspicious. Hence, you cannot join yet. "
                                    f"Check your appearance.",
                        color=guild_embedcolor_member(self, member))
                    embed.set_author(name="AntiRaid | Picturecheck Mode")
                    await member.send(embed=embed)
                    self.bot.cursor.execute(
                        f"SELECT index FROM raidsafemode WHERE guildid = '{member.guild.id}'")
                    safemode = self.bot.cursor.fetchone()
                    if safemode is not None:
                        await member.ban(reason="No Avatar! | Picturecheck mode is Enabled | Safemode is set to High")
                    if safemode is None:
                        await member.kick(reason="No Avatar! | Picturecheck mode is Enabled | Safemode is set to Low")
        except:
            pass

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command()
    async def safemode(self, ctx, state = None):
        if not state:
            self.bot.cursor.execute(
                f"SELECT index FROM raidsafemode WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                embed = discord.Embed(description=f"Safemode is set to **Low** | All AntiRaid Components will **Kick** | To set it to high use {prefix_data(ctx.guild.id)}safemode high", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | SafeMode")
                await ctx.send(embed=embed)
            if result is not None:
                embed = discord.Embed(description=f"Safemode is set to **High** | All AntiRaid Components will **Ban** | To set it to low use {prefix_data(ctx.guild.id)}safemode low", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | SafeMode")
                await ctx.send(embed=embed)
        if state == "high" or state == "High":
            self.bot.cursor.execute(
                f"SELECT index FROM raidsafemode WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                index = random.randint(10, 99)
                sql = ("INSERT INTO raidsafemode(guildid, index) VALUES(%s,%s)")
                val = (str(ctx.guild.id), index)
                self.bot.cursor.execute(sql, val)
                self.bot.connection.commit()
                embed = discord.Embed(description=f"Safemode is now set to **High** | All AntiRaid Components will **Ban** now | To set it to low use {prefix_data(ctx.guild.id)}safemode low", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | SafeMode")
                await ctx.send(embed=embed)
            if result is not None:
                embed = discord.Embed(description=f"Safemode is already **high** | To set it to low use {prefix_data(ctx.guild.id)}safemode low", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | SafeMode")
                await ctx.send(embed=embed)
                return

        if state == "low" or state == "Low":
            self.bot.cursor.execute(
                f"SELECT index FROM raidsafemode WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                embed = discord.Embed(description=f"Safemode is already **low** | To set it to high use {prefix_data(ctx.guild.id)}safemode high", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | SafeMode")
                await ctx.send(embed=embed)
                return
            if result is not None:
                self.bot.cursor.execute(
                    "DELETE FROM raidsafemode WHERE guildid = '{}'".format(ctx.guild.id))
                self.bot.connection.commit()
                embed = discord.Embed(description=f"Safemode is now set to **Low** | All AntiRaid Components will **Kick** now | To set it to high use {prefix_data(ctx.guild.id)}safemode high", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | SafeMode")
                await ctx.send(embed=embed)
                return

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command()
    async def antijoin(self, ctx, state = None):
        if not state:
            self.bot.cursor.execute(
                f"SELECT index FROM antijoin WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                embed = discord.Embed(description=f"Anti-Join is disabled | To enable it {prefix_data(ctx.guild.id)}antijoin enable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Anti-Join")
                await ctx.send(embed=embed)
            if result is not None:
                embed = discord.Embed(description=f"Anti-Join is enabled | To disable it {prefix_data(ctx.guild.id)}antijoin disable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Anti-Join")
                await ctx.send(embed=embed)
        if state == "enable" or state == "Enable" or state == "on":
            self.bot.cursor.execute(
                f"SELECT index FROM antijoin WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                index = random.randint(10, 99)
                sql = ("INSERT INTO antijoin(guildid, index) VALUES(%s,%s)")
                val = (str(ctx.guild.id), index)
                self.bot.cursor.execute(sql, val)
                self.bot.connection.commit()
                embed = discord.Embed(description=f"Anti-Join is now enabled | New Users will be kicked instantly | To disable it {prefix_data(ctx.guild.id)}antijoin disable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Anti-Join")
                await ctx.send(embed=embed)
            if result is not None:
                embed = discord.Embed(description=f"Anti-Join is already enabled | To disable it {prefix_data(ctx.guild.id)}antijoin disable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Anti-Join")
                await ctx.send(embed=embed)
                return
        if state == "disable" or state == "disable" or state == "off":
            self.bot.cursor.execute(
                f"SELECT index FROM antijoin WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                embed = discord.Embed(description=f"Anti-Join is already disabled | To enable it {prefix_data(ctx.guild.id)}antijoin disable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Anti-Join")
                await ctx.send(embed=embed)
                return
            if result is not None:
                self.bot.cursor.execute(
                    "DELETE FROM antijoin WHERE guildid = '{}'".format(ctx.guild.id))
                self.bot.connection.commit()
                embed = discord.Embed(description=f"Anti-Join is now disabled | New Users will not be kicked anymore | To enable it {prefix_data(ctx.guild.id)}antijoin enable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Anti-Join")
                await ctx.send(embed=embed)
                return

    @commands.has_permissions(ban_members=True)
    @commands.bot_has_permissions(ban_members=True)
    @commands.command()
    async def picturecheck(self, ctx, state = None):
        if not state:
            self.bot.cursor.execute(
                f"SELECT index FROM picturecheck WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                embed = discord.Embed(description=f"Picturecheck is disabled | To enable it {prefix_data(ctx.guild.id)}picturecheck enable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Picturecheck Mode")
                await ctx.send(embed=embed)
            if result is not None:
                embed = discord.Embed(description=f"Picturecheck is enabled | To disable it {prefix_data(ctx.guild.id)}picturecheck disable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Picturecheck Mode")
                await ctx.send(embed=embed)
        if state == "enable" or state == "Enable" or state == "on":
            self.bot.cursor.execute(
                f"SELECT index FROM picturecheck WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                index = random.randint(10, 99)
                sql = ("INSERT INTO picturecheck(guildid, index) VALUES(%s,%s)")
                val = (str(ctx.guild.id), index)
                self.bot.cursor.execute(sql, val)
                self.bot.connection.commit()
                embed = discord.Embed(description=f"Picturecheck is now enabled | New Users will be kicked instantly that has no Avatar | To disable it {prefix_data(ctx.guild.id)}picturecheck disable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Picturecheck Mode")
                await ctx.send(embed=embed)
            if result is not None:
                embed = discord.Embed(description=f"Picturecheck is already enabled | To disable it {prefix_data(ctx.guild.id)}picturecheck disable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Picturecheck Mode")
                await ctx.send(embed=embed)
                return
        if state == "disable" or state == "disable" or state == "off":
            self.bot.cursor.execute(
                f"SELECT index FROM picturecheck WHERE guildid = '{ctx.guild.id}'")
            result = self.bot.cursor.fetchone()
            if result is None:
                embed = discord.Embed(description=f"Picturecheck is already disabled | To enable it {prefix_data(ctx.guild.id)}picturecheck disable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Picturecheck Mode")
                await ctx.send(embed=embed)
                return
            if result is not None:
                self.bot.cursor.execute(
                    "DELETE FROM picturecheck WHERE guildid = '{}'".format(ctx.guild.id))
                self.bot.connection.commit()
                embed = discord.Embed(description=f"Picturecheck is now disabled | User without an Avatar will not be kicked anymore | To enable it {prefix_data(ctx.guild.id)}picturecheck enable", color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="AntiRaid | Picturecheck Mode")
                await ctx.send(embed=embed)
                return

def setup(bot):
    bot.add_cog(AntiRaid(bot))
