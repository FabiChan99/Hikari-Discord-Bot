from Utils.data import *
import psycopg2

con = connection = psycopg2.connect(user=PSQLUser(),
                                    password=PSQLPass(),
                                    host=PSQLHost(),
                                    database=PSQLDB())


class CurrencyCog(commands.Cog, name="Currency"):
    """Currency commands."""

    def __init__(self, bot):
        self.bot = bot

    @commands.command(brief="The command to earn coins in the server.")
    async def work(self, ctx):
        main = con
        cursor = main.cursor()
        cursor.execute(f"SELECT time, length FROM cooldown WHERE guild_id = %s AND user_id = %s AND command = %s",
                       (ctx.guild.id, ctx.message.author.id, "work"))
        time_length = cursor.fetchall()
        if time_length:
            time1 = time_length[0][0]
            length = time_length[0][1]
            difference = time.time() - time1
            if difference >= length:
                cursor.execute(
                    "DELETE FROM cooldown WHERE guild_id = %s AND user_id = %s AND command = %s",
                    (ctx.guild.id, ctx.message.author.id, "work"))
                main.commit()
            else:
                embed = discord.Embed(title="Cooldown:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                time_left = length - difference
                hours = time_left // 3600
                mins = (time_left // 60) - (hours * 60)
                secs = time_left % 60
                embed.add_field(name="Time Left:",
                                value='This command is on cooldown, please try again in {:.0f}h {:.0f}m {:.0f}s'.format(
                                    hours, mins, secs))
                await ctx.send(embed=embed)
                return

        member = ctx.message.author
        cursor = main.cursor()
        amount_earned = random.randint(450, 550)
        cursor.execute(f'SELECT coins FROM currency WHERE user_id = {member.id}')
        current_coins = cursor.fetchone()
        if current_coins is None:
            cursor.execute(
                "INSERT into currency(guild_id, user_id, coins, multiplier, daily, company_count) VALUES(%s, %s, %s, %s, %s, %s)",
                (ctx.guild.id, member.id, amount_earned, 1, 0, 0))
            main.commit()
            pass
        else:
            cursor = main.cursor()
            cursor.execute(f"SELECT multiplier FROM currency WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
            multiplier = cursor.fetchone()
            if multiplier is None:
                multiplier = 1
            else:
                multiplier = multiplier[0]
            amount_earned = round(amount_earned * multiplier)
            cursor.execute(f"SELECT coins FROM currency WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
            try:
                current_bal = cursor.fetchone()[0]
            except Exception:
                cursor.execute(
                    "INSERT into currency(guild_id, user_id, coins, multiplier, daily, company_count) VALUES(%s, %s, %s, %s, %s, %s)",
                    (ctx.guild.id, member.id, amount_earned, 1, 0, 0))
                main.commit()
            cursor.execute(
                f"UPDATE currency SET coins = coins + {amount_earned} WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
            main.commit()

        cursor = main.cursor()
        cursor.execute(f"SELECT multiplier FROM currency WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
        multiplier = cursor.fetchone()[0]
        embed = discord.Embed(title="Work:", color=guild_embedcolor_ctx(self, ctx))
        embed.set_thumbnail(url=f'{member.avatar.url}')
        embed.add_field(name="Amount Earned:",
                        value=f"You earned {amount_earned} coins <a:HikariCoin:830790524453650433> with a {multiplier}x multiplier!")

        await ctx.send(embed=embed)

        cursor = main.cursor()
        cursor.execute(f"SELECT user_id FROM cooldown WHERE user_id = %s AND guild_id = %s AND command = %s",
                       (ctx.message.author.id, ctx.guild.id, "work"))
        if cursor.fetchone() is None:
            cursor.execute("INSERT into cooldown(guild_id, user_id, command, length, time) VALUES(%s, %s, %s, %s, %s)",
                           (ctx.guild.id, ctx.message.author.id, "work", 300, int(time.time())))
            main.commit()
        else:
            return

    @commands.command(brief="Displays a specified user's current balance.", aliases=["bal"])
    async def balance(self, ctx, member: discord.Member = None):
        main = con
        if member is None:
            member = ctx.message.author
        cursor = main.cursor()
        cursor.execute(f"SELECT coins FROM currency WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
        current_coins = cursor.fetchone()
        if current_coins is None:
            embed = discord.Embed(title="Current Balance:", color=guild_embedcolor_ctx(self, ctx))
            embed.set_thumbnail(url=f"{member.avatar.url}")
            embed.add_field(name="Coins:", value=f"<@!{member.id}> has 0 coins! <a:HikariCoin:830790524453650433>")
        else:
            embed = discord.Embed(title="Current Balance:", color=guild_embedcolor_ctx(self, ctx))
            embed.set_thumbnail(url=f"{member.avatar.url}")
            embed.add_field(name="Coins:",
                            value=f"<@!{member.id}> has {current_coins[0]} coins! <a:HikariCoin:830790524453650433>")

        await ctx.send(embed=embed)

    @commands.command(brief="Displays the top ten richest users.", aliases=["lb"])
    async def leaderboard(self, ctx):
        main = con
        message = ctx.message
        cursor = main.cursor()
        try:
            cursor.execute(
                f"SELECT user_id, coins from currency WHERE guild_id = {ctx.guild.id} ORDER BY coins DESC LIMIT 10")
        except Exception:
            pass
        result = cursor.fetchall()
        embed = discord.Embed(title="Server Leaderboard:", color=guild_embedcolor_ctx(self, ctx))
        embed.set_thumbnail(url=f"{message.author.avatar.url}")
        for i, x in enumerate(result, 1):
            embed.add_field(name=f"#{i}",
                            value=f"<@!{str(x[0])}> has {str(x[1])} <a:HikariCoin:830790524453650433> coins.",
                            inline=False)
        await ctx.send(embed=embed)

    @commands.command(brief="Displays the top ten richest users.", aliases=["glb"])
    async def gleaderboard(self, ctx):
        main = con
        message = ctx.message
        cursor = main.cursor()
        cursor.execute(f"SELECT user_id, coins from currency ORDER BY coins DESC LIMIT 10")
        result = cursor.fetchall()
        embed = discord.Embed(title="Global Leaderboard:", color=guild_embedcolor_ctx(self, ctx))
        embed.set_thumbnail(url=f"{message.author.avatar.url}")
        for i, x in enumerate(result, 1):
            embed.add_field(name=f"#{i}",
                            value=f"<@!{str(x[0])}> has {str(x[1])} <a:HikariCoin:830790524453650433> coins.",
                            inline=False)
        await ctx.send(embed=embed)

    @commands.command(brief="Allows the user to gamble for coins.")
    async def gamble(self, ctx, bid):
        main = con
        cursor = main.cursor()
        cursor.execute(f"SELECT time, length FROM cooldown WHERE user_id = %s AND guild_id = %s AND command = %s",
                       (ctx.message.author.id, ctx.guild.id, "gamble"))
        time_length = cursor.fetchall()
        if time_length:
            time1 = time_length[0][0]
            length = time_length[0][1]
            difference = time.time() - time1
            if difference >= length:
                cursor.execute("DELETE FROM cooldown WHERE user_id = %s AND guild_id = %s AND command = %s",
                               (ctx.message.author.id, ctx.guild.id, "gamble"))
                main.commit()
            else:
                embed = discord.Embed(title="Cooldown:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                time_left = length - difference
                hours = time_left // 3600
                mins = (time_left // 60) - (hours * 60)
                secs = time_left % 60
                embed.add_field(name="Time Left:",
                                value='This command is on cooldown, please try again in {:.0f}h {:.0f}m {:.0f}s'.format(
                                    hours, mins, secs))
                await ctx.send(embed=embed)
                return

        bid = int(bid)
        cursor = main.cursor()
        cursor.execute(
            f"SELECT coins FROM currency WHERE user_id = {int(ctx.message.author.id)} AND guild_id = {ctx.guild.id}")
        current_coins = cursor.fetchone()

        if current_coins is None:
            embed = discord.Embed(title="Gamble Error:", color=0xFF0000)
            embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
            embed.add_field(name="Description:", value="You have no coins! <a:HikariCoin:830790524453650433>")
            await ctx.send(embed=embed)
            return
        else:
            if bid > int(current_coins[0]):
                embed = discord.Embed(title="Gamble Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Description:",
                                value="You don't have enough coins! <a:HikariCoin:830790524453650433>")
                await ctx.send(embed=embed)
                return
            elif bid <= 0:
                embed = discord.Embed(title="Gamble Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Description:", value="You have no coins! <a:HikariCoin:830790524453650433>")
                await ctx.send(embed=embed)
                return
            else:
                cursor.execute(
                    f"UPDATE currency SET coins = coins - {bid} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                main.commit()
                odds = random.randint(2, 10)
                embed = discord.Embed(title="Gamble:", color=ctx.message.author.color)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="User:", value=f"<@!{ctx.message.author.id}>")
                embed.add_field(name="Bet:", value=f"{bid} <a:HikariCoin:830790524453650433>")
                embed.add_field(name="Odds / Reward:", value=f"1/{odds} for a {odds}x payout.")
                msg = await ctx.send(embed=embed, view=discord.ui.View(
                    discord.ui.Button(label=f'Yes', style=discord.ButtonStyle.green, emoji="✅", custom_id="gamblebet"),
                    discord.ui.Button(label=f'No', style=discord.ButtonStyle.red, emoji="❌", custom_id="gamblenotbet")))
                cursor = main.cursor()
                cursor.execute(f"SELECT user_id FROM cooldown WHERE user_id = %s AND guild_id = %s AND command = %s",
                               (ctx.message.author.id, ctx.guild.id, "gamble"))
                if cursor.fetchone() is None:
                    cursor.execute(
                        "INSERT into cooldown(guild_id, user_id, command, length, time) VALUES(%s, %s, %s, %s, %s)",
                        (ctx.guild.id, ctx.message.author.id, "gamble", 60, int(time.time())))
                    main.commit()
                else:
                    return

                def check_data(message):
                    return message.user == ctx.message.author

                # await msg.add_reaction("✅")
                # await msg.add_reaction("❌")
                interaction = await self.bot.wait_for("interaction", check=check_data, timeout=120)
                if interaction.data["custom_id"] == "gamblebet":
                    if random.randint(1, odds) == 1:
                        winnings = bid * (odds + 1)
                        cursor.execute(
                            f"UPDATE currency SET coins = coins + {winnings} WHERE user_id = {ctx.message.author.id}")
                        main.commit()
                        cursor = main.cursor()
                        cursor.execute(
                            f"SELECT coins FROM currency WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                        current_bal = cursor.fetchone()
                        embed = discord.Embed(title="Gamble:", color=0x00FF00)
                        embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                        embed.add_field(name="Results:",
                                        value=f"You won {winnings} <a:HikariCoin:830790524453650433> coins!",
                                        inline=False)
                        embed.add_field(name="Your new Balance is:",
                                        value=f"{current_bal[0]} <a:HikariCoin:830790524453650433> Coins", inline=False)
                        await msg.edit(embed=embed, view=discord.ui.View(
                            discord.ui.Button(label=f'Yes', style=discord.ButtonStyle.gray, emoji="✅",
                                              custom_id="gamblebet", disabled=True),
                            discord.ui.Button(label=f'No', style=discord.ButtonStyle.gray, emoji="❌",
                                              custom_id="gamblenotbet", disabled=True)))
                        return
                    else:
                        cursor = main.cursor()
                        cursor.execute(
                            f"SELECT coins FROM currency WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                        current_bal = cursor.fetchone()
                        embed = discord.Embed(title="Gamble:", color=0xFF0000)
                        embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                        embed.add_field(name="Results:",
                                        value=f"You lost {bid} <a:HikariCoin:830790524453650433> coins!", inline=False)
                        embed.add_field(name="Your new Balance is:",
                                        value=f"{current_bal[0]} <a:HikariCoin:830790524453650433> Coins", inline=False)
                        await msg.edit(embed=embed, view=discord.ui.View(
                            discord.ui.Button(label=f'Yes', style=discord.ButtonStyle.green, emoji="✅",
                                              custom_id="gamblebet", disabled=True),
                            discord.ui.Button(label=f'No', style=discord.ButtonStyle.red, emoji="❌",
                                              custom_id="gamblenotbet", disabled=True)))
                        return
                else:
                    cursor.execute(
                        f"UPDATE currency SET coins = coins + {bid} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                    main.commit()
                    embed = discord.Embed(title="Gamble:", description=f"{ctx.author.mention} decided to cancel bid",
                                          color=ctx.message.author.color)
                    embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                    await msg.edit(embed=embed, view=discord.ui.View(
                        discord.ui.Button(label=f'Yes', style=discord.ButtonStyle.green, emoji="✅",
                                          custom_id="gamblebet", disabled=True),
                        discord.ui.Button(label=f'No', style=discord.ButtonStyle.red, emoji="❌",
                                          custom_id="gamblenotbet", disabled=True)))

    @gamble.error
    async def gamble_handler(self, ctx, error):
        main = con
        member = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Gamble Error:", color=0xFF0000)
            embed.set_thumbnail(url=f"{member.avatar.url}")
            embed.add_field(name="Missing Bid:", value='Please enter an amount to bid.')
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.command(brief="A shop command where a user can buy upgrades.")
    async def shop(self, ctx):
        enview = discord.ui.View(
            discord.ui.Button(label=f'Raise (1.5x)', style=discord.ButtonStyle.grey, custom_id="raise"),
            discord.ui.Button(label=f'Promotion (2x)', style=discord.ButtonStyle.grey, custom_id="promo"),
            discord.ui.Button(label=f'Assistant (2.5x)', style=discord.ButtonStyle.grey, custom_id="assistant"),
            discord.ui.Button(label=f'Company (3.5x)', style=discord.ButtonStyle.grey, custom_id="company"))
        disview = discord.ui.View(
            discord.ui.Button(label=f'Raise (1.5x)', style=discord.ButtonStyle.grey, custom_id="raise", disabled=True),
            discord.ui.Button(label=f'Promotion (2x)', style=discord.ButtonStyle.grey, custom_id="promo",
                              disabled=True),
            discord.ui.Button(label=f'Assistant (2.5x)', style=discord.ButtonStyle.grey, custom_id="assistant",
                              disabled=True),
            discord.ui.Button(label=f'Company (3.5x)', style=discord.ButtonStyle.grey, custom_id="company",
                              disabled=True))
        main = con
        cursor = main.cursor()
        cursor.execute(
            f"SELECT coins FROM currency WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
        current_coins = cursor.fetchone()
        cursor = main.cursor()
        cursor.execute(
            f"SELECT multiplier FROM currency WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
        current_multiplier = cursor.fetchone()
        if current_multiplier is None:
            current_multiplier = 1
        else:
            current_multiplier = current_multiplier[0]

        if current_coins is None:
            current_coins = 0
        else:
            current_coins = current_coins[0]

        embed = discord.Embed(title="Shop:", color=ctx.message.author.color)
        embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
        embed.add_field(name="#1: Raise (1.5x)", value="75000 coins <a:HikariCoin:830790524453650433>", inline=False)
        embed.add_field(name="#2: Promotion (2x)", value="355000 coins <a:HikariCoin:830790524453650433>", inline=False)
        embed.add_field(name="#3: Assistant (2.5x)", value="895000 coins <a:HikariCoin:830790524453650433>",
                        inline=False)
        embed.add_field(name="#4: Company (3.5x)", value="4.5m coins <a:HikariCoin:830790524453650433>", inline=False)
        msg = await ctx.send(embed=embed, view=enview)

        # await msg.add_reaction(str('1️⃣'))
        # await msg.add_reaction(str('2️⃣'))
        # await msg.add_reaction(str('3️⃣'))
        # await msg.add_reaction(str('4️⃣'))
        def check_data(message):
            return message.user == ctx.message.author

        interaction = await self.bot.wait_for("interaction", check=check_data)
        if interaction.data["custom_id"] == "raise":

            if current_coins < 75000:
                embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Description:", value="You don't have enough coins!")
                await msg.edit(embed=embed, view=disview)
            else:
                cursor.execute(
                    f"UPDATE currency SET coins = coins - {75000} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                cursor.execute(
                    f"UPDATE currency SET multiplier = {1.5} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                main.commit()

                embed = discord.Embed(title="Shop:", color=0x00FF00)
                embed.set_thumbnail(url=f'{ctx.message.author.avatar.url}')
                embed.add_field(name='Purchase:', value="Thank you for purchasing a raise!")
                await msg.edit(embed=embed, view=disview)

        if interaction.data["custom_id"] == "promo":
            if current_multiplier == 1.5:
                if current_coins < 355000:
                    embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                    embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                    embed.add_field(name="Description:", value="You don't have enough coins!")
                    await msg.edit(embed=embed, view=disview)
                else:
                    cursor.execute(
                        f"UPDATE currency SET coins = coins - {355000} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                    cursor.execute(
                        f"UPDATE currency SET multiplier = {2} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                    main.commit()

                    embed = discord.Embed(title="Shop:", color=0x00FF00)
                    embed.set_thumbnail(url=f'{ctx.message.author.avatar.url}')
                    embed.add_field(name='Purchase:', value="Thank you for purchasing a promotion!")
                    await msg.edit(embed=embed, view=disview)
            elif current_multiplier >= 2:
                embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Description:", value="You already have this upgrade!")
                await msg.edit(embed=embed, view=disview)
            else:
                embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Description:", value="You need to buy the previous upgrade!")
                await msg.edit(embed=embed, view=disview)

        if interaction.data["custom_id"] == "assistant":
            if current_multiplier == 2:
                if current_coins < 895000:
                    embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                    embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                    embed.add_field(name="Description:",
                                    value="You don't have enough coins! <a:HikariCoin:830790524453650433>")
                    await msg.edit(embed=embed, view=disview)
                else:
                    cursor.execute(
                        f"UPDATE currency SET coins = coins - {895000} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                    cursor.execute(
                        f"UPDATE currency SET multiplier = {2.5} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                    main.commit()

                    embed = discord.Embed(title="Shop:", color=0x00FF00)
                    embed.set_thumbnail(url=f'{ctx.message.author.avatar.url}')
                    embed.add_field(name='Purchase:', value="Thank you for purchasing an assistant!")
                    await msg.edit(embed=embed, view=disview)
            elif current_multiplier >= 2.5:
                embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Description:", value="You already have this upgrade!")
                await msg.edit(embed=embed, view=disview)
            else:
                embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Description:", value="You need to buy the previous upgrade!")
                await msg.edit(embed=embed, view=disview)

        if interaction.data["custom_id"] == "promo":
            if current_multiplier == 2.5:
                if current_coins < 4500000:
                    embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                    embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                    embed.add_field(name="Description:", value="You don't have enough coins!")
                    await msg.edit(embed=embed, view=disview)
                else:
                    cursor = main.cursor()
                    cursor.execute("SELECT company_count FROM currency WHERE user_id = %s AND guild_id = %s",
                                   (ctx.message.author.id, ctx.guild.id))
                    company_count = cursor.fetchone()
                    if company_count is None:
                        company_count = 0
                    else:
                        company_count = company_count[0]

                    if company_count >= 5:
                        embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                        embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                        embed.add_field(name="Description:",
                                        value="You have reached the maximum amount of companies per user.")
                        await msg.edit(embed=embed, view=disview)
                    else:
                        cursor.execute(
                            f"UPDATE currency SET coins = coins - {4500000} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                        cursor.execute(
                            f"UPDATE currency SET multiplier = {3.5} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                        cursor.execute(
                            f"UPDATE currency SET company_count = {company_count + 1} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                        main.commit()

                        embed = discord.Embed(title="Shop:", color=0x00FF00)
                        embed.set_thumbnail(url=f'{ctx.message.author.avatar.url}')
                        embed.add_field(name='Purchase:', value="Thank you for purchasing a Company!")
                        await msg.edit(embed=embed, view=disview)

                        cursor.execute(
                            "INSERT INTO company(guild_id, user_id, name, stocks, price) VALUES(%s, %s, %s, %s, %s)",
                            (ctx.guild.id, ctx.message.author.id, "Default Company", 100, 1))
                        main.commit()

            elif current_multiplier >= 3.5:
                embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Description:", value="You already have this upgrade!")
                await msg.edit(embed=embed, view=disview)
            else:
                embed = discord.Embed(title="Shop Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Description:", value="You need to buy the previous upgrade!")
                await msg.edit(embed=embed, view=disview)


    @commands.command(brief="Daily reward for currency.", aliases=["d"])
    async def daily(self, ctx):
        main = con
        cursor = main.cursor()

        cursor.execute(f"SELECT coins FROM currency WHERE user_id = {ctx.author.id} AND guild_id = {ctx.guild.id}")
        bal1 = cursor.fetchone()
        if bal1 is None:
            ctx.send(f"You are not in the Database. Please use {prefix_data(ctx.guild.id)}work first!")

        if bal1 is not None:
            pass
        cursor.execute(f"SELECT time, length FROM cooldown WHERE user_id = %s AND guild_id = %s AND command = %s",
                       (ctx.message.author.id, ctx.guild.id, "daily"))
        time_length = cursor.fetchall()
        if time_length:
            time1 = time_length[0][0]
            length = time_length[0][1]
            difference = time.time() - time1
            if difference >= length:
                cursor.execute("DELETE FROM cooldown WHERE user_id = %s AND guild_id = %s AND command = %s",
                               (ctx.message.author.id, ctx.guild.id, "daily"))
                main.commit()
            else:
                embed = discord.Embed(title="Cooldown:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                time_left = length - difference
                hours = time_left // 3600
                mins = (time_left // 60) - (hours * 60)
                secs = time_left % 60
                embed.add_field(name="Time Left:",
                                value='This command is on cooldown, please try again in {:.0f}h {:.0f}m {:.0f}s'.format(
                                    hours, mins, secs))
                await ctx.send(embed=embed)
                return

        cursor = main.cursor()
        cursor.execute(f"SELECT daily FROM currency WHERE user_id = {ctx.message.author.id}")
        current_daily = cursor.fetchone()

        if current_daily is None:
            current_daily = 0
        else:
            current_daily = current_daily[0]

        reward = ((int(current_daily) + 1) * 50000) % 45000
        cursor.execute(
            f"UPDATE currency SET coins = coins + {reward} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
        main.commit()
        embed = discord.Embed(title="Daily Reward:", color=ctx.message.author.color)
        embed.add_field(name=f"You received your daily coins!",
                        value=f"{reward} Coins <a:HikariCoin:830790524453650433>",
                        inline=False)
        embed.set_thumbnail(url=f'{ctx.message.author.avatar.url}')
        await ctx.send(embed=embed)

        cursor = main.cursor()
        cursor.execute(f"SELECT user_id FROM cooldown WHERE user_id = %s AND guild_id = %s AND command = %s",
                       (ctx.message.author.id, ctx.guild.id, "daily"))
        if cursor.fetchone() is None:
            cursor.execute("INSERT into cooldown(guild_id, user_id, command, length, time) VALUES(%s, %s, %s, %s, %s)",
                           (ctx.guild.id, ctx.message.author.id, "daily", 86400, int(time.time())))
            main.commit()
        else:
            return

    @commands.command(brief="Pays a user of your choice coins taken from your balance.", aliases=["g"])
    async def give(self, ctx, member: discord.Member, amount: int):
        main = con
        cursor = main.cursor()
        cursor.execute(
            f"SELECT coins FROM currency WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
        bal = cursor.fetchone()
        if bal is None:
            bal = 0
        else:
            bal = bal[0]

        if amount < 0:
            embed = discord.Embed(title="Give Error:", color=0xFF0000)
            embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
            embed.add_field(name=f"Invalid amount!", value=f"You cannot input negative values.")
            await ctx.send(embed=embed)
            return
        if amount > bal:
            missing = amount - bal
            embed = discord.Embed(title="Give Error:", color=0xFF0000)
            embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
            embed.add_field(name=f"You don't have enough coins!",
                            value=f"Missing {missing} coins. <a:HikariCoin:830790524453650433>")

            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Confirmation:", color=ctx.message.author.color)
        embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
        embed.add_field(name=f"Are you sure you want to give the coins to {member.display_name}?",
                        value=f"Coins: {amount}")
        msg = await ctx.send(embed=embed, view=discord.ui.View(
                    discord.ui.Button(label=f'Yes', style=discord.ButtonStyle.grey, custom_id="yesgive"),
                    discord.ui.Button(label=f'No', style=discord.ButtonStyle.grey, custom_id="nogive")))

        def check_data(message):
            return message.user == ctx.message.author

        interaction = await self.bot.wait_for("interaction", check=check_data)
        if interaction.data["custom_id"] == "yesgive":
            cursor = main.cursor()
            cursor.execute(f"SELECT coins FROM currency WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
            bal1 = cursor.fetchone()
            if bal1 is None:
                print(bal1)
                embed = discord.Embed(title="Give Error:", color=0xFF0000)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name="Receiver has no coins!",
                                value=f"{member.display_name} needs to work at least once.")
                await msg.edit(embed=embed, view=discord.ui.View(
                    discord.ui.Button(label=f'Yes', style=discord.ButtonStyle.grey, custom_id="yesgive", disabled=True),
                    discord.ui.Button(label=f'No', style=discord.ButtonStyle.grey, custom_id="nogive", disabled=True)))
            else:
                cursor.execute(
                    f"UPDATE currency SET coins = coins + {amount} WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
                main.commit()
                cursor.execute(
                    f"UPDATE currency SET coins = coins - {amount} WHERE user_id = {ctx.message.author.id} AND guild_id = {ctx.guild.id}")
                main.commit()
                embed = discord.Embed(title="Coins Given:", color=0x00FF00)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name=f"User {member.display_name} received coins.",
                                value=f"Coins: {amount} <a:HikariCoin:830790524453650433>")

                await msg.edit(embed=embed, view=discord.ui.View(
                    discord.ui.Button(label=f'Yes', style=discord.ButtonStyle.grey, custom_id="yesgive", disabled=True),
                    discord.ui.Button(label=f'No', style=discord.ButtonStyle.grey, custom_id="nogive", disabled=True)))
        if interaction.data["custom_id"] == "nogive":
            embed = discord.Embed(title="Cancelled:", color=0xFF0000)
            embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
            embed.add_field(name=f"User {member.display_name} did not receive coins.", value=f"Command cancelled.")

            await msg.edit(embed=embed, view=discord.ui.View(
                    discord.ui.Button(label=f'Yes', style=discord.ButtonStyle.grey, custom_id="yesgive", disabled=True),
                    discord.ui.Button(label=f'No', style=discord.ButtonStyle.grey, custom_id="nogive", disabled=True)))

    @give.error
    async def give_handler(self, ctx, error):
        member = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Give Error:", color=0xFF0000)
            embed.set_thumbnail(url=f"{member.avatar.url}")
            embed.add_field(name="Missing Bid:", value='Please enter all required arguments (user, amount).')
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.command(brief="Set a name for your company.")
    async def name_company(self, ctx, *, name: str):
        main = con
        cursor = main.cursor()
        cursor.execute("SELECT name FROM company WHERE user_id = %s AND guild_id = %s",
                       (ctx.message.author.id, ctx.guild.id))
        current_name = cursor.fetchone()
        if current_name is None:
            embed = discord.Embed(title="Company:", color=0xFF0000)
            embed.set_thumbnail(url=f'{ctx.author.avatar.url}')
            embed.add_field(name="Name Change Failure:", value=f"You need to buy the CEO upgrade to have a company!")
            await ctx.send(embed=embed)
        else:
            cursor.execute("UPDATE company SET name = %s WHERE user_id = %s AND guild_id = %s",
                           (name, ctx.message.author.id, ctx.guild.id))
            main.commit()
            await ctx.send("Company name changed!")

    @name_company.error
    async def namecompany_handler(self, ctx, error):
        member = ctx.message.author
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(title="Company Error:", color=0xFF0000)
            embed.set_thumbnail(url=f"{member.avatar.url}")
            embed.add_field(name="Missing Argument:", value='Name to name your Company!')
            await ctx.send(embed=embed)
        else:
            raise error

    @commands.command(brief="View information on a company.")
    async def company(self, ctx, member: discord.Member = None):
        if member is None:
            member = ctx.message.author
        main = con
        cursor = main.cursor()
        cursor.execute("SELECT name, stocks, price FROM company WHERE user_id = %s AND guild_id = %s",
                       (member.id, ctx.guild.id))
        info = cursor.fetchall()
        if info:
            name = info[0][0]
            stocks = info[0][1]
            price = info[0][2]
        else:
            embed = discord.Embed(title="Company Error:", color=0xFF0000)
            embed.set_thumbnail(url=f'{ctx.author.avatar.url}')
            embed.add_field(name="Description:", value=f"This user does not own a company!")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Company:", color=guild_embedcolor_ctx(self, ctx))
        embed.set_thumbnail(url=f'{ctx.author.avatar.url}')
        embed.add_field(name="Name:", value=f"{name}", inline=False)
        embed.add_field(name="Shares:", value=f"{stocks}", inline=False)
        embed.add_field(name="Price per Stock:", value=f"{price} coin(s)", inline=False)
        await ctx.send(embed=embed)

    @commands.command(brief="Sell a company you own.")
    async def sell_company(self, ctx):
        main = con
        cursor = main.cursor()

        cursor.execute("SELECT name, stocks, price FROM company WHERE user_id = %s AND guild_id = %s",
                       (ctx.message.author.id, ctx.guild.id))
        info = cursor.fetchall()
        if info:
            name = info[0][0]
            stocks = info[0][1]
            price = info[0][2]
        else:
            embed = discord.Embed(title="Company Error:", color=0xFF0000)
            embed.set_thumbnail(url=f'{ctx.author.avatar.url}')
            embed.add_field(name="Description:", value=f"You do not own a company to sell!")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Company:", color=ctx.author.color)
        embed.set_thumbnail(url=f'{ctx.author.avatar.url}')
        embed.add_field(name="Name:", value=f"{name}", inline=False)
        embed.add_field(name="Shares:", value=f"{stocks}", inline=False)
        embed.add_field(name="Price per Stock:", value=f"{price} coin(s) <a:HikariCoin:830790524453650433>",
                        inline=False)
        embed.add_field(name="Confirmation:",
                        value=f"Are you sure you want to sell this company for {stocks * price * 1000}? (There is a maximum of five companies per user.)",
                        inline=True)
        msg = await ctx.send(embed=embed)
        await msg.add_reaction("✅")
        await msg.add_reaction("❌")
        reaction1, user1 = await self.bot.wait_for("reaction_add", check=lambda reaction, user: user == ctx.author)
        if str(reaction1.emoji) == "✅":
            cursor.execute("DELETE FROM company WHERE user_id = %s AND guild_id = %s",
                           (ctx.message.author.id, ctx.guild.id))
            cursor.execute("UPDATE currency SET multiplier = %s WHERE user_id = %s AND guild_id = %s",
                           (2.5, ctx.message.author.id, ctx.guild.id))
            main.commit()
            cursor = main.cursor()
            cursor.execute("SELECT company_count FROM currency WHERE user_id = %s AND guild_id = %s",
                           (ctx.message.author.id, ctx.guild.id))
            company_count = cursor.fetchone()
            if company_count is None:
                company_count = 0
            else:
                company_count = company_count[0]

            embed = discord.Embed(title="Company:", color=0x00FF00)
            embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
            embed.add_field(name=f"You sold your company.", value=f"{5 - company_count} companies left.")

            await msg.edit(embed=embed)

        else:
            embed = discord.Embed(title="Cancelled:", color=0xFF0000)
            embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
            embed.add_field(name=f"You did not sell your company.", value=f"Command cancelled.")

            await msg.edit(embed=embed)

    @commands.command(brief="Increase the amount of shares in your company.")
    async def company_stock(self, ctx):
        member = ctx.message.author
        main = con
        cursor = main.cursor()
        cursor.execute("SELECT stocks, price FROM company WHERE user_id = %s AND guild_id = %s",
                       (member.id, ctx.guild.id))
        info = cursor.fetchall()
        if info:
            stocks = info[0][0]
            price = info[0][1]
        else:
            embed = discord.Embed(title="Company Error:", color=0xFF0000)
            embed.set_thumbnail(url=f'{ctx.author.avatar.url}')
            embed.add_field(name="Description:", value=f"This user does not own a company!")
            await ctx.send(embed=embed)
            return

        embed = discord.Embed(title="Company value:", color=guild_embedcolor_ctx(self, ctx))
        embed.set_thumbnail(url=f'{ctx.author.avatar.url}')
        embed.add_field(name="Shares:", value=f"{stocks}", inline=False)
        embed.add_field(name="Price per Stock:", value=f"{price} coin(s)", inline=False)
        embed.add_field(name="Amount added:", value="How many shares would you like to add? ", inline=True)
        await ctx.send(embed=embed)

        msg = await self.bot.wait_for('message')
        total_price = 0
        if msg.author.id == member.id:
            if msg.content.isdigit():
                amount = int(msg.content)

                if amount + stocks > 5000:
                    embed = discord.Embed(title="Company Error:", color=0xFF0000)
                    embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                    embed.add_field(name=f"Invalid amount!", value=f"You cannot have more than 5000 shares.")
                    await ctx.send(embed=embed)
                    return
                if amount < 0:
                    embed = discord.Embed(title="Company Error:", color=0xFF0000)
                    embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                    embed.add_field(name=f"Invalid amount!", value=f"You cannot input negative values.")
                    await ctx.send(embed=embed)
                    return
                for i in range(amount):
                    price = price - (price / stocks)
                    total_price = total_price + (price * 10)
                    stocks = stocks + 1

                price = round(price, 2)

                cursor = main.cursor()
                cursor.execute(f"SELECT coins FROM currency WHERE user_id = {member.id} AND guild_id = {ctx.guild.id}")
                current_coins = cursor.fetchone()[0]
                if total_price > current_coins:
                    missing = total_price - current_coins
                    embed = discord.Embed(title="Company Error:", color=0xFF0000)
                    embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                    embed.add_field(name="You don't have enough coins to add that amount of shares:",
                                    value=f"Missing {missing} coins.")
                    await msg.edit(embed=embed)
                    return

                embed = discord.Embed(title="Confirmation:", color=ctx.message.author.color)
                embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                embed.add_field(name=f"Are you sure you want to add {amount} shares?",
                                value=f"New Price: {price} \n New Share Amount: {stocks}")
                msg = await ctx.send(embed=embed)
                await msg.add_reaction("✅")
                await msg.add_reaction("❌")
                reaction1, user1 = await self.bot.wait_for("reaction_add",
                                                           check=lambda reaction, user: user == ctx.author)
                if str(reaction1.emoji) == "✅":
                    cursor.execute(f"UPDATE company SET stocks = {stocks} WHERE user_id = %s AND guild_id = %s",
                                   (member.id, ctx.guild.id))
                    cursor.execute(f"UPDATE company SET price = {price} WHERE user_id = %s AND guild_id = %s",
                                   (member.id, ctx.guild.id))
                    cursor.execute(
                        f"UPDATE currency SET coins = coins - {total_price} WHERE user_id = %s AND guild_id = %s",
                        (member.id, ctx.guild.id))
                    main.commit()
                    embed = discord.Embed(title="Shares Added: ", color=guild_embedcolor_ctx(self, ctx))
                    embed.set_thumbnail(url=f'{ctx.author.avatar.url}')
                    embed.add_field(name="Amount: ", value=f"You added {amount} shares", inline=False)
                    embed.add_field(name="Price:", value=f"{price} coin(s) <a:HikariCoin:830790524453650433>",
                                    inline=False)
                    embed.add_field(name="Shares:", value=f"{stocks}", inline=False)
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title="Cancelled:", color=0xFF0000)
                    embed.set_thumbnail(url=f"{ctx.message.author.avatar.url}")
                    embed.add_field(name=f"No shares added: ", value=f"Command cancelled.")

                    await msg.edit(embed=embed)


def setup(bot):
    bot.add_cog(CurrencyCog(bot))
