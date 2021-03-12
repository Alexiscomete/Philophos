import discord, sqlite3
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command(aliases=['inv'])
    async def inventory(self, ctx):
        embed = discord.Embed(title=f"Inventaire de {ctx.author.name}", description=ctx.author.mention, color=0x000000)
        embed.add_field(name="BIENTÔT DISPONIBLE", value="** **", inline=False)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("inventory")