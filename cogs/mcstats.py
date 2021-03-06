import discord
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def mcstats(self, ctx, ip = None):
        if ip == None:
            await ctx.send("N'oublie pas l'IP du serveur Minecraft !")
        else:
            embed = discord.Embed(title="Ping d'un serveur Minecraft")
            embed.add_field(name=f"IP : {ip}", value="** **", inline=False)
            embed.set_image(url=f"http://status.mclive.eu/{ip}/{ip}/25565/banner.png")
            await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("mcstats")