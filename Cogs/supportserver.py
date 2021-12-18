# import
import discord

from Utils.data import *


# class
class SupportServer(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):
        if member.guild.id == 811743610746830850:
            await member.add_roles(member.guild.get_role(811746939305197628))
            embed = discord.Embed(timestamp=datetime.datetime.utcnow(), description=f"Welcome to the Hikari Support Server! To get support go to <#811746969328287774>. If you want  to receive update notifications, head over to <#818514290813435945>.", color=guild_embedcolor_member(self, member))
            channel = self.bot.get_channel(811746966018195506)
            embed.set_footer(text="Joined at")
            embed.set_author(name=member.name, icon_url=member.avatar.url)
            embed.set_thumbnail(url=member.guild.icon.url)
            await channel.send(embed=embed, content=member.mention)

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        channel = self.bot.get_channel(821320188426453002)
        em = discord.Embed(title="Added in a new guild!",
                           description=f"**Guild** : `{guild.name} ({guild.id})`\n\n**Guild members** : `{guild.member_count}`\n\n**Owner** : `{guild.owner}` - (`{guild.owner_id}`)\n\n**Guild region** : `{guild.region}`\n\n**Guild created at** : `{guild.created_at}`",
                           color=color_data())
        await channel.send(embed=em)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        channel = self.bot.get_channel(821320188426453002)
        em = discord.Embed(title=f"Got removed from `{guild.name} ({guild.id})`..", color=color_data())
        await channel.send(embed=em)

def setup(bot):
    bot.add_cog(SupportServer(bot))
