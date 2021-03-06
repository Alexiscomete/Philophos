import discord, urllib.request, requests, json
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def search(self, ctx):
        espace = " "
        search_mc = ctx.message.content.split(" ")
        if len(search_mc) == 1 or len(search_mc) == 2:
            await ctx.send("N'oublie pas d'arguments ! (Plus d'informations : **+help search**)")
        else:
            async with ctx.channel.typing():
                if search_mc[1] == "uuid" or search_mc[1] == "pseudo":
                    embed = discord.Embed(title=f"Recherche d'un pseudo/UUID d'un utilisateur")
                    if search_mc[1].lower() == "uuid":
                        try:
                            search_api = requests.get(f"https://minecraft-api.com/api/uuid/{espace.join(search_mc[2:])}/json").json()
                        except json.decoder.JSONDecodeError:
                            await ctx.send("Vérifie si le pseudo, ou le UUID, est correct.")
                        embed.add_field(name="Pseudo du joueur :", value=espace.join(search_mc[2:]), inline=False)
                        embed.add_field(name="UUID du joueur :", value=search_api['uuid'], inline=False)
                        skin_api_body = requests.get(f"https://minecraft-api.com/api/skins/{espace.join(search_mc[2:])}/body/10.5/10/json").json()
                    elif search_mc[1].lower() == "pseudo":
                        try:
                            search_api = requests.get(f"https://minecraft-api.com/api/pseudo/{search_mc[2]}/json").json()
                        except json.decoder.JSONDecodeError:
                            await ctx.send("Vérifie si le pseudo, ou le UUID, est correct.")
                        embed.add_field(name="Pseudo du joueur :", value=search_api['pseudo'], inline=False)
                        embed.add_field(name="UUID du joueur :", value=search_mc[2], inline=False)
                        skin_api_body = requests.get(f"https://minecraft-api.com/api/skins/{search_api['pseudo']}/body/10.5/10/json").json()
                    avatar_url = urllib.request.urlretrieve(f"data:image/png;base64,{skin_api_body['skin']}", "images/search_skin_body.png")
                    file = discord.File("/root/discord-bots/AmanagerX/images/search_skin_body.png", filename="search_skin_body.png")
                    embed.set_thumbnail(url="attachment://search_skin_body.png")
                else:
                    await ctx.send("N'oublie pas d'arguments ! (UUID ou pseudo, avec ensuite l'UUID ou le pseudo du joueur.)")
            await ctx.send(file=file, embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("search")