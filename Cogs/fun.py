# import
import operator
from typing import Optional

from Utils.data import *
from discord.ext.commands import clean_content
import io
import random
import discord
import datetime
import requests
from discord.ext import commands
from discord.ext.commands import errors, converter

editsnipe_message_author = {}
editsnipe_message_content = {}
snipe_message_author = {}
snipe_message_content = {}
SYLLABLE = "([aeiouyAEIOUY]|[0-9]|[ ])"


# class
class Fun(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # snipe
    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if not message.author.bot:
            try:
                snipe_message_author[message.channel.id] = message.author
                snipe_message_content[message.channel.id] = message.content
                await asyncio.sleep(120)
                del snipe_message_author[message.channel.id]
                del snipe_message_content[message.channel.id]
            except Exception:
                pass

    # snipe
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if not before.author.bot:
            try:
                editsnipe_message_author[before.channel.id] = before.author
                editsnipe_message_content[before.channel.id] = before.content
                await asyncio.sleep(120)
                del editsnipe_message_author[before.channel.id]
                del editsnipe_message_content[before.channel.id]
            except:
                pass

        # funfacts

    @commands.command(aliases=['fact', 'funfacts', 'fakt'])
    async def funfact(self, ctx):
        if ctx.guild.id == 750365461945778209:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://api.hikaribot.me:6969/funfact") as response:
                    topic_list = await response.text()
            embed = discord.Embed(description=str(topic_list), color=color_data())
            embed.set_author(name="Funfact!", icon_url=ctx.author.avatar.url)
            await ctx.send(embed=embed)
            return

    @commands.cooldown(1, 30, commands.BucketType.guild)
    @commands.command()
    async def topic(self, ctx):
        if ctx.guild.id == 750365461945778209 or ctx.guild.preferred_locale == "de":
            if ctx.channel.id == 771174633230827540:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://api.hikaribot.me:6969/topic/en") as response:
                        topic_list = await response.text()
                embed = discord.Embed(description=str(topic_list), color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="A new Topic was requested!", icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
                return
            else:
                async with aiohttp.ClientSession() as session:
                    async with session.get(f"http://api.hikaribot.me:6969/topic/de") as response:
                        topic_list = await response.text()
                embed = discord.Embed(description=str(topic_list), color=guild_embedcolor_ctx(self, ctx))
                embed.set_author(name="Neues Thema wurde angefragt!", icon_url=ctx.author.avatar.url)
                await ctx.send(embed=embed)
                return
        else:
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://api.hikaribot.me:6969/topic/en") as response:
                    topic_list = await response.text()
            embed = discord.Embed(description=str(topic_list), color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name="A new Topic was requested!", icon_url=ctx.author.avatar.url)
            await ctx.message.reply(embed=embed, mention_author=False)
            return

    @commands.command()
    async def snipe(self, ctx):
        channel = ctx.channel
        try:  # This piece of code is run if the bot finds anything in the dictionary
            embed = discord.Embed(title=f"Last deleted message in #{channel.name}",
                                  description=snipe_message_content[channel.id], color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(
                text=f"The message was sent by: {snipe_message_author[channel.id]} | Sniped by: {ctx.author}\n This message deletes itself in 20 Seconds")
            msg = await ctx.message.reply(embed=embed, mention_author=False)
            await asyncio.sleep(20)
            await msg.delete()
        except:  # This piece of code is run if the bot doesn't find anything in the dictionary
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.add_field(name="Sad...",
                            value="Why do you snipe? Here is nothing to snipe <a:AGC_kekboom:825053807300837389>")
            msg = await ctx.message.reply(embed=embed, mention_author=False)
            await asyncio.sleep(20)
            await msg.delete()
            return

    @commands.command()
    async def editsnipe(self, ctx):
        channel = ctx.channel
        try:
            embed = discord.Embed(title=f"Last edited message in #{channel.name}",
                                  description=editsnipe_message_content[channel.id],
                                  color=guild_embedcolor_ctx(self, ctx))
            embed.set_footer(
                text=f"The message was edited by: {editsnipe_message_author[channel.id]} | Sniped by: {ctx.author}\n This message deletes itself in 20 Seconds")
            msg = await ctx.message.reply(embed=embed, mention_author=False)
            await asyncio.sleep(20)
            await msg.delete()
        except:  # This piece of code is run if the bot doesn't find anything in the dictionary
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.add_field(name="Sad...",
                            value="Why do you snipe? Here is nothing to snipe <a:AGC_kekboom:825053807300837389>")
            msg = await ctx.message.reply(embed=embed, mention_author=False)
            await asyncio.sleep(20)
            await msg.delete()
            return

    @commands.command(description="Shows a random meme")
    async def meme(self, ctx):
        BASEURLS = ["https://meme-api.herokuapp.com/gimme", "https://meme-api.herokuapp.com/gimme/pcmemes", "https://meme-api.herokuapp.com/gimme/softwaregore", "https://meme-api.herokuapp.com/gimme/techsupportgore", "https://meme-api.herokuapp.com/gimme/animemes"]

        URL = random.choice(BASEURLS)



        def check_valid_status_code(request):
            if request.status_code == 200:
                return request.json()

            return False

        def get_meme():
            request = requests.get(URL)
            data = check_valid_status_code(request)
            return data

        memee = get_meme()
        if not memee:
            await ctx.channel.send("Couldn't get meme from API. Try again later.")
        else:
            caption = memee["title"]
            img = memee["url"]
            nsfw = memee["nsfw"]
            spoiler = memee["spoiler"]
            if nsfw == "true" or spoiler == "true":
                await self.meme(ctx)
            else:
                embed = discord.Embed(title=f"{caption}", color=guild_embedcolor_ctx(self, ctx)
                                      )
                embed.set_image(url=f"{img}")
#                embed.set_footer(
#                    text=f"Requested By: {ctx.author.name}",
#                    icon_url=f"{ctx.author.avatar.url}",
#                )
                msg1 = await ctx.send(embed=embed, view=discord.ui.View(
                    discord.ui.Button(label=f'New Meme', style=discord.ButtonStyle.grey, custom_id="newmeme")))

                def check_data(message):
                    return message.channel == ctx.message.channel

                try:
                    interaction = await self.bot.wait_for("interaction", check=check_data, timeout=60)
                    if interaction.data["custom_id"] == "newmeme":
                        await msg1.edit(embed=embed, view=discord.ui.View(
                            discord.ui.Button(label=f'New Meme', style=discord.ButtonStyle.grey, custom_id="newmeme",
                                              disabled=True)))
                        await self.meme(ctx)
                except asyncio.TimeoutError:
                    await msg1.edit(embed=embed, view=discord.ui.View(
                        discord.ui.Button(label=f'use {prefix_data(ctx.guild.id)}meme for new meme',
                                          style=discord.ButtonStyle.grey,
                                          disabled=True)))

    # ship

    @commands.command(aliases=['trump', 'trumpquote'])
    async def asktrump(self, ctx, *, question):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                    f'https://api.whatdoestrumpthink.com/api/v1/quotes/personalized?q={question}') as resp:
                file = await resp.json()
        quote = file['message']
        em = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
        em.title = "What does Trump say?"
        em.description = quote
        em.set_footer(text="Made possible by whatdoestrumpthink.com")
        await ctx.message.reply(embed=em, mention_author=False)

    @commands.command()
    async def catfact(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://catfact.ninja/fact") as response:
                fact = (await response.json())["fact"]
                length = (await response.json())["length"]
                embed = discord.Embed(title=f'Random Cat Fact Number: **{length}**', description=f'Cat Fact: {fact}',
                                      colour=guild_embedcolor_ctx(self, ctx))
                embed.set_footer(text="")
                await ctx.message.reply(embed=embed, mention_author=False)
                await session.close()


def setup(bot):
    bot.add_cog(Fun(bot))
