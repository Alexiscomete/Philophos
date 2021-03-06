import discord, random
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def color(self, ctx, color = None):
        if color == None:
            await ctx.send(f"{ctx.author.mention} N'oublie pas le code héxadécimal !")
        else:
            hexsearch = color.replace("#",'').upper()
            embed = discord.Embed(title=f"Sélecteur de couleurs", description=f"Couleur recherchée : **#{hexsearch}**")
            embed.set_image(url=f"https://www.colorhexa.com/{hexsearch}.png")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("8ball")