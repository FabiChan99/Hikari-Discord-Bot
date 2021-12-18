# import
import discord

from Utils.data import *


# class
class Mod(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def userpurge(self, ctx, limit=None, member: discord.User = None):
        if not limit:
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"A required argument is missing",
                             icon_url=cross_icon())
            embed.add_field(name=f'> Usage:', value=f'{prefix()}userpurge [amount] [user]')
            await ctx.message.reply(embed=embed, mention_author=False)
            return
        else:
            await ctx.message.delete()
            msg = []
            try:
                limit = int(limit)
            except:
                return await ctx.message.reply("Please provide an amount.")
            if not member:
                await ctx.channel.purge(limit=limit)
                return await ctx.send(
                    f"Successfully deleted `{limit}` messages. This message will be deleted in **10s**.",
                    delete_after=10)
            if limit == 1:
                await ctx.channel.purge(limit=limit)
                return await ctx.send(
                    f"Successfully deleted `{limit}` message from **{member.mention}**. This message will be deleted in **10s**.",
                    delete_after=10)
            async for m in ctx.channel.history():
                if len(msg) == limit:
                    break
                if m.author == member:
                    msg.append(m)
            await ctx.channel.delete_messages(msg)
            await ctx.send(
                f"Successfully deleted `{limit}` messages from **{member.mention}**. This message will be deleted in **10s**.",
                delete_after=10)
            return

    # purge
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(manage_messages=True)
    @commands.command(aliases=['prune', 'clear'])
    async def purge(self, ctx, value: int = None):
        '''Deletes Messages'''
        if value:
            try:
                limited = min(int(value), 200)
                await ctx.channel.purge(limit=limited, before=ctx.message)

                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"I have successfully deleted {limited} messages", icon_url=chop_icon())
                if value > 200:
                    embed.add_field(name=f'> Note:', value=f'The Purgelimit is 200')
                await ctx.message.reply(embed=embed, delete_after=10, mention_author=False)
                await ctx.message.delete()
                return
            except Exception:
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"A Error has Occoured", icon_url=cross_icon())
                embed.add_field(name=f'> Information:',
                                value=f'Looks like i don´t have enough permissions or there is a bug. Please Contact: {self.bot.get_user(developer()).name}')
                await ctx.send(embed=embed, mention_author=False)
                return
        else:
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"I don't know how much messages i should delete!", icon_url=cross_icon())
            embed.add_field(name=f'> Usage:', value=f'{prefix()}purge [value]')
            await ctx.message.reply(embed=embed, mention_author=False)
            return

    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def unban(self, ctx, member: discord.User = None, reason = None):
        try:
            user = await self.bot.fetch_user(member.id)
            await ctx.guild.unban(user, reason=f"Unban is executed by: {ctx.author} | Reason: {reason}")
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"Unbanned {user.name} successfully", icon_url=chop_icon())
            await ctx.send(embed=embed)
        except discord.NotFound:
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"{user.name} is not banned!", icon_url=cross_icon())
            await ctx.send(embed=embed)

    # kick
    @commands.bot_has_permissions(kick_members=True)
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def kick(self, ctx, user: discord.Member = None, *, reason=None):
        if user:
            try:

                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"You got kicked from {ctx.guild.name}", icon_url=ctx.guild.icon.url)
                embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                await user.send(embed=embed)
                if reason:
                    embed.add_field(name=f'> Reason:', value=reason)
                    await user.kick(reason='Reason: "{}" | By Mod: {}'.format(reason, ctx.author))
                await user.kick(reason=' By Mod: {}'.format(ctx.author))
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"{user.name} kicked successfully", icon_url=chop_icon())
                await ctx.message.reply(embed=embed, mention_author=False)
                return
            except Exception:
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"A Exception occurred", icon_url=cross_icon())
                embed.add_field(name=f'> Information:',
                                value=f'I am lacking the permissions or its a bug! For support join the support server')
                await ctx.message.reply(embed=embed, mention_author=False)
                return
        else:
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"You have not specified a user. I don't know who to kick",
                             icon_url=cross_icon())
            embed.add_field(name=f'> Usage:', value=f'{prefix()}kick [user] [reason]')
            await ctx.message.reply(embed=embed, mention_author=False)
            return

    # slowmode
    @commands.command(aliases=["setdelay", "cooldown"])
    @commands.bot_has_permissions(manage_messages=True)
    @commands.has_permissions(kick_members=True)
    async def slowmode(self, ctx, seconds: int):
        await ctx.channel.edit(slowmode_delay=seconds)
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Channel Cooldown", icon_url=chop_icon())
        embed.add_field(name=f"Information", value=f'I set the cooldown to {seconds} seconds!')
        await ctx.message.reply(embed=embed, mention_author=False)

    # ban

    @commands.bot_has_permissions(ban_members=True)
    @commands.has_permissions(ban_members=True)
    @commands.command()
    async def ban(self, ctx, user: discord.User = None, *, reason=None):
        if user:
            try:
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"You got banned from {ctx.guild.name}", icon_url=ctx.guild.icon.url)
                embed.add_field(name="Reason:", value=f"{reason}", inline=False)
                if ctx.guild.id == 750365461945778209:
                    embed.add_field(name="Du möchtest einen Entbannungsantrag stellen?",
                                    value=f"Beantrage eine Entbannung [Hier](https://unban.animegamingcafe.de)")
                try:
                    await user.send(embed=embed)
                    sent = "Yes"
                except Exception as e:
                    print(e)
                    sent = "No, because i can\'t sent messages to this user."
                    pass
                if reason:
                    embed.add_field(name=f'> Reason:', value=reason)
                    await ctx.guild.ban(user, reason='Reason: "{}" | By Mod: {}'.format(reason, ctx.author))
                else:
                    await ctx.guild.ban(user, reason='By Mod: {}'.format(ctx.author))
                if reason is None: reason = "No reason provided"
                embed = discord.Embed(description=f"The reason was: {reason}", color=guild_embedcolor_ctx(self, ctx))

                embed.set_author(name=f"Banned {user.name} successfully", icon_url=chop_icon())
                embed.set_footer(text=f"User got notified: {sent}")
                await ctx.message.reply(embed=embed, mention_author=False)
                return
            except Exception:
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"Something went wrong", icon_url=cross_icon())
                embed.add_field(name=f'> Information:',
                                value=f'I am lacking the permissions or its a bug! For support join the support server')
                await ctx.message.reply(embed=embed, mention_author=False)
                return
        else:
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"You have not specified a user. I don't know who to ban",
                             icon_url=cross_icon())
            embed.add_field(name=f'> Usage:', value=f'{prefix()}ban [user] [reason]')
            await ctx.message.reply(embed=embed, mention_author=False)
            return

    # warn
    @commands.has_permissions(kick_members=True)
    @commands.command()
    async def warn(self, ctx, user: discord.Member = None, *, reason=None):
        if user:
            try:

                if user.bot:
                    return
                if user.id == self.bot.user.id:
                    return
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"You have been warned on {ctx.guild.name}", icon_url=ctx.guild.icon.url)
                if reason:
                    embed.add_field(name=f'> Reason:', value=reason)
                await user.send(embed=embed)
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"{user.name} was warned", icon_url=chop_icon())
                if reason:
                    embed.add_field(name=f'> Reason:', value=reason)
                await ctx.message.reply(embed=embed, mention_author=False)
                return
            except Exception:
                embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name=f"Something went wrong", icon_url=cross_icon())
                embed.add_field(name=f'> Information:',
                                value=f'Check if the bot has enough permissions or contact {self.bot.get_user(developer()).name}')
                await ctx.message.reply(embed=embed, mention_author=False)
                return
        else:
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"The user I should warn is missing", icon_url=cross_icon())
            embed.add_field(name=f'> Usage:', value=f'{prefix()}warn [user] [reason]')
            await ctx.message.reply(embed=embed, mention_author=False)
            return

    # Mute
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def mute(self, ctx, member: discord.Member, *, reason=None):
        if ctx.author.top_role.position <= member.top_role.position:
            return
        guild = ctx.guild
        mutedRole = discord.utils.get(guild.roles, name="Muted")
        if not mutedRole:
            mutedRole = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(mutedRole, speak=False, send_messages=False)
        await member.add_roles(mutedRole, reason=reason)
        try:
            embed1 = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed1.set_author(name=f"You got permanently muted from {ctx.guild.name}")
            embed1.add_field(name="Reason:", value=f"{reason}", inline=False)
            await member.send(embed=embed1)
        except Exception:
            pass
        embed2 = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed2.set_author(name=f"{member.name} got permanently muted!")
        embed2.add_field(name="Reason:", value=f"{reason}", inline=False)
        await ctx.message.reply(embed=embed2, mention_author=False)

    # Unmute
    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def unmute(self, ctx, member: discord.Member):
        mutedrole = discord.utils.get(ctx.guild.roles, name="Muted")
        await member.remove_roles(mutedrole)
        embed1 = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        try:
            embed1.set_author(name=f"You got unmuted on {ctx.guild.name}")
            embed3 = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        except Exception:
            pass
        await member.send(embed=embed1)
        embed3.set_author(name=f"{member.name} got unmuted!")
        await ctx.message.reply(embed=embed3, mention_author=False)


def setup(bot):
    bot.add_cog(Mod(bot))
