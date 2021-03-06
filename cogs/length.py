import discord
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def length(self, ctx, *, texte):
        embed = discord.Embed(title=f"Compteur de caractères")
        embed.add_field(name="Nombre de caractères :", value=f"{len(list(str(texte)))}", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("length")