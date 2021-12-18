# import
from Utils.data import *


# class
class Utilities(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    # ping
    @commands.command()
    async def ping(self, ctx):
        workingcm = f"<:HikariCheckmark:822416199291895848>"
        try:
            ping = ctx.message
            embed = discord.Embed(description=f"**Bot Latency**", color=guild_embedcolor_ctx(self, ctx), timestamp=ctx.message.created_at)
            embed.add_field(name=f"<:HikariMessageLatency:821783592853962764> Message Latency:",
                            value=f"<a:HikariLoading:822433462141190166> Polling...",
                            inline=False)
            embed.add_field(name=f"<:HikariGateLatency:821783197908992062> Gateway Latency:",
                            value=f"<a:HikariLoading:822433462141190166> Polling...",
                            inline=False)
            embed.add_field(name=f"<:HikariMongoDB:821719219620020255> MongoDB Database Latency:",
                            value=f"<a:HikariLoading:822433462141190166> Polling...", inline=False)
            embed.add_field(name=f"<:HikariPostgreSQL:822064847624732683> PostgreSQL Database Latency:",
                            value=f"<a:HikariLoading:822433462141190166> Polling...", inline=False)
            embed.add_field(name=f"<:HikariAPI:822079436177408022> API Latency:",
                            value=f"<a:HikariLoading:822433462141190166> Polling...", inline=False)
            pong = await ctx.send(embed=embed, mention_author=False)
            delta = pong.created_at - ping.created_at
            delta = f"{workingcm} {int(delta.total_seconds() * 1000)} ms"
        except Exception:
            delta = f"<:HikariServiceError:822406064989405185> Failed"
            pass

        try:
            start_mongodb = perf_counter()
            prefix_db.find_one({"_id": str(ctx.guild.id)})
            end_mongodb = perf_counter()
            mongolatency = f"{workingcm} {round((end_mongodb - start_mongodb) * 1000)} ms"
        except Exception:
            mongolatency = f"<:HikariServiceError:822406064989405185> Failed"
            pass

        try:
            gw_latency = f"{workingcm} {round(self.bot.latency * 1000)} ms"
        except Exception:
            gw_latency = f"<:HikariServiceError:822406064989405185> Failed"
            pass
        try:
            start_psql = perf_counter()

            self.bot.cursor.execute("SELECT version();")
            self.bot.cursor.fetchone()
            end_psql = perf_counter()
            psql_latency = f"{workingcm} {round((end_psql - start_psql) * 1000)} ms"
        except Exception:
            psql_latency = f"<:HikariServiceError:822406064989405185> Failed"
            pass
        try:
            start_apilatency = perf_counter()
            async with aiohttp.ClientSession() as session:
                async with session.get(f"http://api.hikaribot.me:6969/hug") as response:
                    image = await response.text()
            end_apilatency = perf_counter()
            apilatency = f"{workingcm} {round((end_apilatency - start_apilatency) * 1000)} ms"
        except Exception:
            apilatency = f"<:HikariServiceError:822406064989405185> Failed"
            pass
        shard_ping_list = ""
        for shard_pings in self.bot.latencies:
            shard_ping_list += f"Shard {shard_pings[0]}: **{round(shard_pings[1]* 1000)}** ms\n"
        embed = discord.Embed(description=f"**Bot Latency**", color=guild_embedcolor_ctx(self, ctx), timestamp=ctx.message.created_at)
        embed.add_field(name=f"<:HikariMessageLatency:821783592853962764> Message Latency:", value=f"{delta}",
                        inline=False)
        embed.add_field(name=f"<:HikariGateLatency:821783197908992062> Gateway Latency:", value=f"{gw_latency}",
                        inline=False)
        embed.add_field(name=f"<:HikariMongoDB:821719219620020255> MongoDB Database Latency:",
                        value=f"{mongolatency}", inline=False)
        embed.add_field(name=f"<:HikariPostgreSQL:822064847624732683> PostgreSQL Database Latency:",
                        value=f"{psql_latency}", inline=False)
        embed.add_field(name=f"<:HikariAPI:822079436177408022> API Latency:",
                        value=f"{apilatency}", inline=False)
        embed.add_field(name=f"Shard Latencies", value=shard_ping_list, inline=False)
        await asyncio.sleep(5)
        await pong.edit(embed=embed)
        return



    # addvote
    @commands.command(aliases=['addvotes'])
    async def addvote(self, ctx, votecount='bool'):
        if votecount.lower() == 'bool':
            emote_list = ['✅', '❌']
        elif votecount in ['2', '3', '4', '5', '6', '7', '8', '9', '10']:
            emotes = ['1\u20e3', '2\u20e3', '3\u20e3', '4\u20e3', '5\u20e3', '6\u20e3', '7\u20e3', '8\u20e3', '9\u20e3',
                      '\U0001f51f']
            emote_list = []
            for i in range(0, int(votecount)):
                emote_list.append(emotes[i])
        else:
            ctx.say(':x: Enter a Number between 2 and 10')

        message = await ctx.channel.history(limit=1, before=ctx.message).flatten()
        try:
            await ctx.message.delete()
        except:
            pass

        for emote in emote_list:
            await message[0].add_reaction(emote)



def setup(bot):
    bot.add_cog(Utilities(bot))
