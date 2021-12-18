#import
from Utils.data import *
#class
class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot




# help
    @commands.group()
    async def help(self, ctx):
        if ctx.invoked_subcommand is None:
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"My Commands", icon_url=self.bot.user.avatar.url)
            embed.add_field(name=f'<:HikariInfo:830793552865787924> Info Commands | For help: `{prefix_data(ctx.guild.id)}help info`', value=f'`avatar, banner, serverinfo, userinfo, botinvite, vote, stats, uptime`', inline=False)
            embed.add_field(name=f'<:HikariPepeJail:830794184868626433> Jailing Commands', value=f'`jail, unjail, setupjail, unsetupjail`', inline=False)
            embed.add_field(name=f'<a:AGC_yameteban:787808225709916190> Moderation Commands | For help: `{prefix_data(ctx.guild.id)}help mod`', value=f'`ban, unban, idban, unban, kick, purge, slowmode, mute, unmute`', inline=False)
            embed.add_field(name=f'<a:Pepe_Ban:836314279748567041> Auto-Moderation Commands', value=f'`imageonly, badword, antiinvite`', inline=False)
            embed.add_field(name=f'<:HikariCuddle:830793168848027720> Roleplay Commands', value=f'`love, hug, cuddle, kiss, slap, lick, kill, cry, poke, bite, blush, punch, sip, wave`', inline=False)
            embed.add_field(name=f'<a:HikariPepeSearch:830792858477920316> Search Commands', value=f'`anime, manga, urban`', inline=False)
            embed.add_field(name=f'<:HikariUser:839912865027588106> Profile Commands', value=f'`profile, marry, divorce, partner`', inline=False)
            embed.add_field(name=f'<:HikariFunny:830794437759205386> Fun Commands', value=f'`snipe, editsnipe, trump, meme, bored, catfact, topic`', inline=False)
            embed.add_field(name=f'<a:HikariZahnrad:830794737300144140> Utility Commands', value=f'`afk, suggest, ping, prefix, vote`', inline=False)
            #embed.add_field(name=f'🎮 Game Stats Commands (More Soon)', value=f'`osu`', inline=False)
            embed.add_field(name=f'🕹️ Activtys [BETA] Uses Discords Activity (Youtube Together and more) Feature', value=f'`startyt, activity`', inline=False)
            embed.add_field(name=f'<:AGC_MonkaChrist:777932456707751956> Anti-Raid Commands', value=f'`antijoin, picturecheck, safemode`', inline=False)
            #embed.add_field(name=f'🎵 Music Commands', value=f'`play, skip, disconnect, shuffle, pause, resume, volume`', inline=False)
            embed.add_field(name=f'<a:HikariCoin:830790524453650433> Economy Commands | For help: `{prefix_data(ctx.guild.id)}help eco`', value=f'`balance, work, daily (only use it when u used work before), give, shop, gamble, leaderboard, gleaderboard, sell_company, company_stock, company, name_company`', inline=False)
            embed.add_field(name=f'<a:Welcome:786340736743505980> Custom Welcome Commands', value=f'For Setup: `setwelc`', inline=False)
            #embed.add_field(name=f'<:HikariLeveling:830796310134259764> Leveling Commands', value=f'`rank, levels` | To configure Level up reward ranks: `{prefix_data(ctx.guild.id)}ranks`', inline=False)
            embed.add_field(name=f'<:HikariSettings:838435700407402528> Settings Commands', value=f'`reactonping, embedcolor`', inline=False)
            embed.set_footer(text=f'My Prefix: {prefix_data(ctx.guild.id)} | Version: {version()} | For help of a command enter: {prefix_data(ctx.guild.id)}help <command> | for botsupport enter: h!support and join our support server')
            await ctx.message.reply(embed=embed, mention_author=False, view=discord.ui.View(discord.ui.Button(label=f'Support Server', style=discord.ButtonStyle.grey, url="https://discord.gg/cUykgYfh4F"), discord.ui.Button(label=f'Invite Hikari', style=discord.ButtonStyle.grey, url="https://discord.com/oauth2/authorize?client_id=811742311692238860&permissions=1073217527&scope=applications.commands%20bot")))



    @help.command()
    async def info(self, ctx):
        embed = discord.Embed(description=f"<a:HikariCoin:830790524453650433> Command usages:", color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Info Help ", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}avatar', value=f'Shows the Avatar for a user', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}serverinfo', value=f'Shows some infomations about this Guild', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}userinfo', value=f'Shows some infos about a user', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}botinvite', value=f'Retrives the current OAuth2 Invite Link', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}vote', value=f'Shows the TopGG Voting Link for me', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}gamble', value=f'Gambles some Money | Usage: `{prefix_data(ctx.guild.id)}gamble <coins>`', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}stats', value=f'Shows Stats about the Bot', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return

    @help.command(aliases=["economy"])
    async def eco(self, ctx):
        embed = discord.Embed(description=f"<a:HikariCoin:830790524453650433> Command usages:", color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Economy Help ", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}balance', value=f'Shows your balance or the balance of a User', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}work', value=f'Earn some Coins', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}daily', value=f'Earn Daily Coins (only use it when u used work before)', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}give', value=f'Gives Coins to a user', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}shop', value=f'Opens the shop where you can buy Upgrades', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}gamble', value=f'Gambles some Money | Usage: `{prefix_data(ctx.guild.id)}gamble <coins>`', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}gleaderboard', value=f'Shows the global leaderboard', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}leaderboard', value=f'Shows the Server leaderboard', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}company', value=f'Shows your company', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return

    @help.command(aliases=["moderation"])
    async def mod(self, ctx):
        embed = discord.Embed(description=f"<a:HikariCoin:830790524453650433> Command usages:", color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Moderation Help ", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}ban', value=f'Bans a Member', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}idban', value=f'Bans a User if its not in the Guild anymore with the User ID', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}unban', value=f'Unbans a User', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}kick', value=f'Kicks a Member', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}purge', value=f'Bulk delete Messages', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}slowmode', value=f'Sets slowmode in the current Channel', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}mute', value=f'Mutes a Member', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}unmute', value=f'Unmutes a Member', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return

    @help.command(aliases=["settings"])
    async def setting(self, ctx):
        embed = discord.Embed(description=f"<:HikariSettings:838435700407402528> Command usages:", color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Settings Help ", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}reactonping', value=f'Enable/Disable that the Bot will respond if you mention her', inline=False)
        embed.add_field(name=f'> {prefix_data(ctx.guild.id)}embedcolor', value=f'Change the Embed Color', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def avatar(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Gets the Avatar of a User", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}avatar <user>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def serverinfo(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Gets Infomation of the current Server", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}serverinfo', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def userinfo(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Gets Infomation of a User", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}userinfo <user>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command(aliases=["botinvite"])
    async def invite(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Gets gets my Invite", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}invite', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def ban(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Bans a User", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}ban <user|id> <reason>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return

    @help.command()
    async def unban(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Unbans a User", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}unban <id>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return

    @help.command()
    async def idban(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Bans a User thats not in the guild", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}idban <id> <reason>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return

    @help.command()
    async def kick(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Kicks a User", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}kick <user|id> <reason>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def purge(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Purges messages in the current channels (max 200 messages at once)", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}purge <amount>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def slowmode(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Kicks a User", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}kick <user|id> <reason>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def anime(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Gets Infomations about an anime", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}anime <animename>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def manga(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Gets Infomations about an manga", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}manga <manganame>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def snipe(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Bring back a deleted message (30 seconds or the message is lost)", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}snipe', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def catfact(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Shows a random fact about cats", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}catfact', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def trump(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"What would trump say?", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}trump <word>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def meme(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Gets a random meme from Reddit", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}meme', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return


    @help.command()
    async def bored(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Gives you activitys to dont be bored anymore", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}bored <amount of peoples (1-8)>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return

    @help.command()
    async def suggest(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Sends a suggestion to the Developers Server", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}suggest <your suggestion>', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return





    @help.command()
    async def ping(self, ctx):
        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        embed.set_author(name=f"Calculate the Ping to the Discord Gateways", icon_url=self.bot.user.avatar.url)
        embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}ping', inline=False)
        await ctx.message.reply(embed=embed, mention_author=False)
        return




def setup(bot):
    bot.add_cog(Help(bot))
