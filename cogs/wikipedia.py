import discord, wikipedia, asyncio
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wikipedia(self, ctx):
        def check(msg):
            return msg.author == ctx.author and msg.channel == ctx.channel

        wikipedia.set_lang("fr")
        wikipedia_msg = ctx.message.content.split(" ")
        espace, wikicontent_elements, bs_n, n, numbers = " ", [], "\n", 0, [':one:', ':two:', ':three:', ':four:', ':five:', ':six:', ':seven:', ':eight:', ':nine:', ':keycap_ten:']
        if len(wikipedia_msg) == 1:
            await ctx.send(f"{ctx.author.mention} N'oublie pas de spécifier un sujet à rechercher ! (Plus d'infos : **+help wikipedia**)")
        else:
            if wikipedia_msg[1] == "random":
                async with ctx.channel.typing():
                    wikipedia_choice_made = wikipedia.random(pages=1)
                    pagetext = wikipedia.summary(wikipedia_choice_made, sentences=3, chars=2000)
                    embed = discord.Embed(title=f"Recherche Wikipédia", description=f"Recherche sur **{wikipedia_choice_made}**", color=0x808080)
                    embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/frwiki.png")
                await ctx.send(embed=embed, content=">>> " + pagetext)
            else:
                wikicontent = wikipedia.search(espace.join(wikipedia_msg[1:]), results=10, suggestion=False)
                if not wikicontent:
                    embed = discord.Embed(title=f"Recherche Wikipédia", color=0xe74c3c)
                    embed.add_field(name="Désolé, mais aucune recherche n'a été trouvée sur ce que vous avez entré...", value=espace.join(wikipedia_msg[1:]))
                    embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/frwiki.png")
                    await ctx.send(embed=embed)
                else:
                    embed = discord.Embed(title=f"Recherche Wikipédia", description="Faites un choix parmi ci-dessous, tu as 10 secondes.", color=0xffffff)
                    for element in wikicontent:
                        embed.add_field(name=numbers[n] + " " + element, value="** **", inline=False)
                        n += 1
                    wikipedia_choice = await ctx.send(embed=embed)
                    try:
                        msg = await self.client.wait_for("message", check=check, timeout=10)
                    except asyncio.TimeoutError:
                        await wikipedia_choice.edit(embed=None, content=f"{ctx.author.mention} Tu as mis trop de temps pour répondre...")
                    try:
                        choice = int(msg.content)
                    except ValueError:
                        await wikipedia_choice.edit(embed=None, content=f"{ctx.author.mention} Le choix n'est pas valide... Ça n'est pas un nombre !")
                    if 1 <= choice <= 10:
                        wikipedia_choice_made = wikicontent[choice-1]
                        embed = discord.Embed(title=f"Recherche Wikipédia", description=f"Recherche sur **{wikipedia_choice_made}**", color=0xffffff)
                        try:
                            pagetext = wikipedia.summary(wikipedia_choice_made, sentences=3, chars=2000)
                        except wikipedia.exceptions.PageError:
                            await wikipedia_choice.edit(embed=None, content=f"{ctx.author.mention} Cette page n'a pas pu être chargée... (la page n'a pas été trouvée [BUG])")
                        except wikipedia.exceptions.DisambiguationError:
                            await wikipedia_choice.edit(embed=None, content=f"{ctx.author.mention} Cette page n'a pas pu être chargée... (ça n'était pas assez précis [BUG])")
                        embed.set_thumbnail(url="https://www.wikipedia.org/static/images/project-logos/frwiki.png")
                        await msg.delete()
                        await wikipedia_choice.edit(embed=embed, content=">>> " + pagetext)
                    else:
                        await wikipedia_choice.edit(embed=None, content=f"{ctx.author.mention} Le choix n'est pas valide... Le nombre est plus petit que 1 ou plus grand que 10 !")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("wikipedia")