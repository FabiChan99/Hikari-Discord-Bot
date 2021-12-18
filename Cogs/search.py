# import


from Utils.data import *


# class
class Utility(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.command()
    async def anime(self, ctx, *, anime: str):
        """Search AniList for anime"""
        query = """
        query ($search: String) {
            Media (search: $search, type: ANIME) {
                id
                title {
                    romaji
                    english
                    native
                }
                description
                episodes
                duration
                status
                genres
                averageScore
                coverImage {
                    large
                }
            }
        }
        """

        variables = {"search": anime}

        response = requests.post(
            "https://graphql.anilist.co", json={"query": query, "variables": variables}
        )

        rateLimitRemaining = int(response.headers["X-RateLimit-Remaining"])

        # Rate limiting is currently set to 90 requests per minute
        # If you go over the rate limit you'll receive a 1-minute timeout
        # https://anilist.gitbook.io/anilist-apiv2-docs/overview/rate-limiting
        if rateLimitRemaining > 0:
            animeJSON = response.json()["data"]["Media"]

            description = animeJSON["description"]
            description = description.replace("<br>", "")
            genres = ""
            for g in animeJSON["genres"]:
                genres += "{}, ".format(g)

            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx),
                title="{} / {}".format(
                    animeJSON["title"]["romaji"], animeJSON["title"]["native"]
                ),
                url="https://anilist.co/anime/{}".format(animeJSON["id"]),
                description=description
            )
            embed.set_thumbnail(url=animeJSON["coverImage"]["large"])

            embed.add_field(
                name="Episode Count", value=animeJSON["episodes"], inline=True
            )
            embed.add_field(
                name="Duration",
                value="{} minutes per episode".format(animeJSON["duration"]),
                inline=True,
            )
            embed.add_field(name="Status", value=animeJSON["status"], inline=True)
            embed.add_field(name="Genres", value=genres[:-2], inline=True)
            embed.add_field(
                name="Average Score", value=animeJSON["averageScore"], inline=True
            )

            embed.set_footer(text="Powered by anilist.co")
            await ctx.message.reply(embed=embed, mention_author=False)
        else:
            await ctx.message.reply(
                "The bot is currently being rate limited :( Try again in {} seconds".format(
                    response.headers["Retry-After"]
                )
            )

    # manga
    @commands.command()
    async def manga(self, ctx, *, mangaName: str = None):
        if mangaName:
            api = 'https://graphql.anilist.co'
            query = '''
            query ($name: String){
              Media(search: $name, type: MANGA) {
                id
                idMal
                description
                title {
                  romaji
                  english
                }
                coverImage {
                  large
                }
                startDate {
                  year
                  month
                  day
                }
                endDate {
                  year
                  month
                  day
                }
                status
                chapters
                volumes
                averageScore
                meanScore
                genres
                tags {
                  name
                }
                siteUrl
              }
            }
            '''
            variables = {
                'name': mangaName
            }

            async with aiohttp.ClientSession() as session:
                async with session.post(api, json={'query': query, 'variables': variables},
                                        headers=self.bot.userAgentHeaders) as r:
                    if r.status == 200:
                        json = await r.json()
                        data = json['data']['Media']

                        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                        embed.set_footer(text='API provided by AniList.co | ID: {}'.format(str(data['id'])))
                        embed.set_thumbnail(url=data['coverImage']['large'])
                        if data['title']['english'] == None or data['title']['english'] == data['title']['romaji']:
                            embed.add_field(name='Title', value=data['title']['romaji'], inline=False)
                        else:
                            embed.add_field(name='Title',
                                            value='{} ({})'.format(data['title']['english'], data['title']['romaji']),
                                            inline=False)
                        # embed.add_field(name='Beschreibung', value=data['description'], inline=False)
                        if data['chapters'] != None:
                            # https://github.com/AniList/ApiV2-GraphQL-Docs/issues/47
                            embed.add_field(name='Chapters', value=data['chapters'], inline=True)
                            embed.add_field(name='Volumes', value=data['volumes'], inline=True)
                        embed.add_field(name='Started',
                                        value='{}.{}.{}'.format(data['startDate']['day'], data['startDate']['month'],
                                                                data['startDate']['year']), inline=True)
                        if data['endDate']['day'] != None:
                            embed.add_field(name='Ended',
                                            value='{}.{}.{}'.format(data['endDate']['day'], data['endDate']['month'],
                                                                    data['endDate']['year']), inline=True)
                        embed.add_field(name='Status', value=data['status'].replace('_', ' ').title(), inline=True)
                        embed.add_field(name='Ø Score', value=data['averageScore'], inline=True)
                        embed.add_field(name='Genres', value=', '.join(data['genres']), inline=False)
                        tags = ''
                        for tag in data['tags']:
                            tags += tag['name'] + ', '
                        embed.add_field(name='Tags', value=tags[:-2], inline=False)
                        embed.add_field(name='AniList Link', value=data['siteUrl'], inline=False)
                        embed.add_field(name='MyAnimeList Link',
                                        value='https://myanimelist.net/anime/' + str(data['idMal']), inline=False)
                        await ctx.message.reply(embed=embed, mention_author=False)

                    else:
                        embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
                        embed.set_author(name="Can´t find the provided Manga", icon_url=cross_icon())
                        await ctx.message.reply(embed=embed, mention_author=False)
        else:
            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.set_author(name=f"You don´t provided a Manga. I can´t read your Mind.",
                             icon_url=cross_icon())
            embed.add_field(name=f'> Usage:', value=f'{prefix_data(ctx.guild.id)}manga [name]')
            await ctx.message.reply(embed=embed, mention_author=False)
            return

    @commands.command(aliases=["ud"])
    async def urban(self, ctx, *, term: str):
        try:
            req = requests.get(
                "http://api.urbandictionary.com/v0/define?term={}".format(term)
            )

            dictTerm = req.json()
            dictTerm = dictTerm["list"][0]

            word = dictTerm["word"]
            definition = dictTerm["definition"]
            example = dictTerm["example"]
            message = "{} \n\n *{}*".format(definition, example)


            message = message.replace("[", "")
            message = message.replace("]", "")

            embed = discord.Embed(color=guild_embedcolor_ctx(self, ctx))
            embed.add_field(name=word, value=message, inline=False)

            await ctx.message.reply(embed=embed, mention_author=False)
        except Exception:
            embed = discord.Embed(description=f"An exception occurred", color=guild_embedcolor_ctx(self, ctx), icon_url=cross_icon())
            embed.set_author(name=f"Urbandictionary", icon_url=cross_icon())
            await ctx.message.reply(embed=embed, mention_author=False)

    async def cog_command_error(self, ctx: commands.Context, error: commands.CommandError):
        embed = discord.Embed(color=0xEE0000)
        embed.set_author(name=f"Error!", icon_url=cross_icon())
        embed.add_field(name=f'> Information:', value='{}'.format(error))
        await ctx.message.reply(embed=embed, mention_author=False)

def setup(bot):
    bot.add_cog(Utility(bot))
