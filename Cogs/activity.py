# class

from Utils.data import *


activity_list1 = [['<:youtube:853997774084505621>', 'youtube'],
                 ['<:poker:853997774475362324>', 'poker'],
                 ['<:betrayal:853997774155284492>', 'betrayal']]

activity_list2 = [['<:fishing:853997774269186099>', 'fishing'],
                 ['<:chess:853997774332756008>', 'chess'],
                 ['<:chess:853997774332756008>', 'Beta Youtube']]

class Activity(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.togetherControl = DiscordTogether(bot)


    @commands.command(aliases=["startyt"])
    async def activity(self, ctx):
            try:
                embed = discord.Embed(title='Start your game activity now!',
                                      description=f'__Note the following things when using the bot:__\n **-** This message only creates links for the current voice channel <#{ctx.author.voice.channel.id}>"\n**-** This Function is BETA\n**-**To start the activity click on the link that was sent after selecting the game',
                                      color=guild_embedcolor_ctx(self, ctx)
    )
                embed.set_thumbnail(url=self.bot.user.avatar.url)
                initemb = embed
                embed.set_footer(text=f'Choose which activity you want to start | Only valid for {ctx.author.voice.channel.name}')
                initmsg = await ctx.send(embed=embed, view=discord.ui.View(discord.ui.Button(label=f'Youtube', style=discord.ButtonStyle.grey, custom_id="youtube"),
                                                                           discord.ui.Button(label=f'Poker Night', style=discord.ButtonStyle.grey, custom_id="poker"),
                                                                           discord.ui.Button(label=f'Betrayal', style=discord.ButtonStyle.grey, custom_id="betrayal"),
                                                                           discord.ui.Button(label=f'Fishington.io', style=discord.ButtonStyle.grey, custom_id="fishing"),
                                                                           discord.ui.Button(label=f'Doodlecrew', style=discord.ButtonStyle.grey, custom_id="doodle"),
                                                                           discord.ui.Button(label=f'LetterTile', style=discord.ButtonStyle.grey, custom_id="letter"),
                                                                           discord.ui.Button(label=f'Chess', style=discord.ButtonStyle.grey, custom_id="chess"),
                                                                           discord.ui.Button(label=f'Beta Youtube', style=discord.ButtonStyle.grey, custom_id="betayt"),

                                                                           )



                                         )
            except Exception as e:
                print(e)
                embed = discord.Embed(color=0x0f29d1
    )
                embed.set_author(name="You are not in a voice channel.",
                                 icon_url='https://cdn.discordapp.com/emojis/828650661704499262.png?v=1')
                await ctx.send(embed=embed,
                               delete_after=30)
                return
            timeout = time.time() + 60 * 10
            while True:
                if time.time() > timeout:
                    break

                def check_data(message):
                    return message.user == ctx.message.author


                interaction = await self.bot.wait_for("interaction", check=check_data, timeout=600)

                try:
                    if not ctx.author.voice.channel.id:
                        embed = discord.Embed(color=0x0f29d1
    )
                        embed.set_author(name="You are not in a voice channel.",
                                         icon_url='https://cdn.discordapp.com/emojis/861266772724023296.png?size=96')
                        await interaction.respond(embed=embed,
                                                  delete_after=30)
                except Exception:
                    embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx)
    )
                    embed.set_author(name="You are not in a voice channel.",
                                     icon_url='https://cdn.discordapp.com/emojis/861266772724023296.png?size=96')
                    await interaction.respond(embed=embed,
                                              delete_after=30)
                if interaction.data["custom_id"] == "youtube":
                    link = await self.togetherControl.create_link(ctx.author.voice.channel.id, "youtube")

                if interaction.data["custom_id"] == "poker":
                    link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 755827207812677713)
                if interaction.data["custom_id"] == "betrayal":
                    link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 814288819477020702)
                if interaction.data["custom_id"] == "fishing":
                    link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 814288819477020702)
                if interaction.data["custom_id"] == "chess":
                    link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 832012774040141894)
                if interaction.data["custom_id"] == "betayt":
                    link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 880218394199220334)
                if interaction.data["custom_id"] == "letter":
                    link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 879863686565621790)
                if interaction.data["custom_id"] == "doodle":
                    link = await self.togetherControl.create_link(ctx.author.voice.channel.id, 878067389634314250)
                #await initmsg.delete()

                embed = discord.Embed(description=f'[Click here]({link}) to start the game activity or use the link that was sent along.',
                                      color=guild_embedcolor_ctx(self, ctx)
    )
                embed.set_author(name='Here is your activity link',
                                 icon_url='https://cdn.discordapp.com/emojis/828650661972672623.png?v=1')
                embed.set_footer(text=f'This link is bound to {ctx.author.voice.channel.name}')
                await interaction.channel.send(embed=embed,
                                          content=link)




def setup(bot):
    bot.add_cog(Activity(bot))
