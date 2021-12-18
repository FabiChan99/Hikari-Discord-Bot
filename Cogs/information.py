# import
from discord import commands
from discord.ext import commands
from Utils.data import cooldown, guild_embedcolor_ctx, version, start_time, developer, prefix_data, converter, time_syntax
import discord
from datetime import datetime
import platform
import asyncio
import psutil
# class
class Information(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    #discord.utils.format_dt(member.created_at, style='R')

    @commands.cooldown(cooldown()[0], cooldown()[1], commands.BucketType.user)
    @commands.command(aliases=['botinfo', 'info', 'uptime', 'bot', 'stats'])
    async def status(self, ctx):
        '''Shows infos about the Bot'''
        #print(start_time)
        uptime_stamp = discord.utils.format_dt(start_time, style='R')
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=(f"{self.bot.user.name}\'s info"))
        embed.add_field(name='Bot ID:', value=self.bot.user.id, inline=False)
        embed.add_field(name='Developer:',
                        value=f'<:HikariDev:811912295067287572> {self.bot.get_user(developer())}', inline=True)
        embed.add_field(name='Version:', value=version(), inline=True)
        embed.add_field(name="Library:", value=f"py-cord {discord.__version__}", inline=True)
        embed.add_field(name='Prefix:', value=prefix_data(ctx.guild.id), inline=True)
        system = str(platform.system())
        if system == 'Windows':
            system = '<:HikariWindows:811766717155770371> Windows'
        if system == 'Linux':
            system = '<:HikariLinux:816634128542859305> Linux'
        embed.add_field(name="Platform", value=system, inline=True)
        embed.add_field(name='Commands:', value=str(len(self.bot.commands)), inline=True)
        embed.add_field(name='Servers:', value=f'<:ServerHikari:811911412979859476> {str(len(self.bot.guilds))}',
                        inline=True)
        embed.add_field(name='Modules:', value=str(len(self.bot.cogs)), inline=True)
        embed.add_field(name='Users:', value=str(sum(g.member_count for g in self.bot.guilds)), inline=True)
        embed.add_field(name="Stats for developer", value=str(
            f"  **Shards:** {self.bot.shard_count} \n **CPU:** {psutil.cpu_percent()}% \n **RAM:** {converter(psutil.virtual_memory().used)}B/{converter(psutil.virtual_memory().total)}B ({psutil.virtual_memory().percent}%)\n **DISK:** {converter(psutil.disk_usage('/').used)}B/{converter(psutil.disk_usage('/').total)}B ({psutil.disk_usage('/').percent}%)"),
                        inline=True)
        embed.add_field(name="Bot's online since:", value=f'{uptime_stamp}',
                        inline=False)
        embed.set_thumbnail(url=self.bot.user.avatar.url)
        await ctx.send(embed=embed)
        return


    # avatar
    @commands.bot_has_permissions(send_messages=True, embed_links=True, read_message_history=True)
    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.message.author if not member else member
        if not member:
            member = ctx.message.author
        else:
            member = member
        embed_user = discord.Embed(title=f"Avatar of {member.name}", color=guild_embedcolor_ctx(self, ctx))
        embed_user.set_image(url=member.avatar.url)
        embed_display = discord.Embed(title=f"Display Avatar of {member.name}", color=guild_embedcolor_ctx(self, ctx))
        embed_display.set_image(url=member.display_avatar.url)
        embed_user.set_footer(text=f"Requested by {ctx.author}")
        embed_display.set_footer(text=f"Requested by {ctx.author}")
        if member.guild_avatar:
            main_msg = await ctx.send(embed=embed_user, view=discord.ui.View(
                discord.ui.Button(label=f'Display Avatar', style=discord.ButtonStyle.grey,
                                  custom_id="Display Avatar")))
        else:
            main_msg = await ctx.send(embed=embed_user, view=discord.ui.View(
                discord.ui.Button(label=f'Display Avatar', style=discord.ButtonStyle.grey,
                                  custom_id="Display Avatar", disabled=True)))

        def check_data(message):
            return message.user == ctx.message.author

        while True:
            try:
                interaction = await self.bot.wait_for("interaction", check=check_data, timeout=600)
            except asyncio.TimeoutError:
                await main_msg.edit(embed=embed_user, view=discord.ui.View())
                break
            if interaction.type == discord.InteractionType.component:
                if interaction.data["custom_id"] == "Display Avatar":
                    await main_msg.edit(embed=embed_display, view=discord.ui.View(
                        discord.ui.Button(label=f'User Avatar', style=discord.ButtonStyle.grey,
                                          custom_id="User Avatar")))
                if interaction.data["custom_id"] == "User Avatar":
                    await main_msg.edit(embed=embed_user, view=discord.ui.View(
                        discord.ui.Button(label=f'Display Avatar', style=discord.ButtonStyle.grey,
                                          custom_id="Display Avatar")))


    # serverinfos
    @commands.command(pass_context=True, aliases=['serverinfo', 'guild', 'membercount'])
    async def server(self, ctx):
        '''Gibt Informationen über die derzeitge Discord Guild aus'''
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))  # Golden
        embed.set_thumbnail(url=ctx.guild.icon.url)
        embed.add_field(name='Name', value=ctx.guild.name, inline=True)
        embed.add_field(name='ID', value=ctx.guild.id, inline=True)
        embed.add_field(name='Owner', value=ctx.guild.owner, inline=True)
        embed.add_field(name='Region', value=ctx.guild.region, inline=True)
        embed.add_field(name='Member', value=ctx.guild.member_count, inline=True)
        embed.add_field(name='Boosts', value=ctx.guild.premium_subscription_count, inline=True)
        embed.add_field(name='Language', value=ctx.guild.preferred_locale, inline=True)
        embed.add_field(name='Created on', value=discord.utils.format_dt(ctx.guild.created_at, style='R'), inline=True)
        embed.add_field(name='Bans', value=len(await ctx.guild.bans()), inline=True)
        if ctx.guild.banner:
            embed.set_image(url=ctx.guild.banner.url)
        await ctx.message.reply(embed=embed, mention_author=False)
        return

    @commands.command()
    async def banner(self, ctx, member: discord.Member = None):
        if not member:
            member = ctx.author
        member = await self.bot.fetch_user(member.id)
        if member.banner is None:
            embed = discord.Embed(description=f"{member} has no Banner", color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"Banner of {member.name}")
            embed.set_footer(text=f"Requested by {ctx.author}")
            await ctx.reply(embed=embed, mention_author=False)
            return
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_image(url=member.banner.url)
        embed.set_author(name=f"Banner of {member.name}")
        embed.set_footer(text=f"Requested by {ctx.author}")
        await ctx.reply(embed=embed, mention_author=False)


    # whois

    @commands.command(aliases=["userinfo"])
    async def whois(self, ctx, member: discord.Member = None):

        if member == None:
            member = ctx.author

        if member.top_role.is_default():
            topRole = 'everyone'  # to prevent @everyone spam
            topRoleColour = '#000000'
        else:
            topRole = member.top_role
            topRoleColour = member.top_role.colour

        if member is not None:
            embed = discord.Embed(color=member.top_role.colour)
            embed.set_footer(text=f'UserID: {member.id}')
            embed.set_thumbnail(url=member.avatar.url)
            if member.name != member.display_name:
                fullName = f'{member} ({member.display_name})'
            else:
                fullName = member
            embed.add_field(name=member.name, value=fullName, inline=False)


            embed.add_field(name='Account created:',
                            value=f"{discord.utils.format_dt(member.created_at, style='R')}", inline=False)

            embed.add_field(name='Server joined at:',
                            value=f"{discord.utils.format_dt(member.joined_at, style='R')}", inline=False)
            embed.add_field(name='Avatar Link', value=f"[Klick here for the Avatar Link!]({member.avatar.url})",
                            inline=False)
            # embed.add_field(name="Roles:", value="".join([role.mention + "\n" for role in member.roles]))
            embed.add_field(name='Rolecolor', value='{} ({})'.format(topRoleColour, topRole), inline=True)
            embed.add_field(name='Status', value=member.status, inline=True)
            member = await self.bot.fetch_user(member.id)
            if member.banner is not None:
                embed.set_image(url=member.banner.url)
            await ctx.message.reply(embed=embed, mention_author=False)
            return

def setup(bot):
    bot.add_cog(Information(bot))
