import discord
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def me(self, ctx, *, action = None):
        if action == None:
            action = "ne fait rien."
        embed = discord.Embed(description=f"{ctx.author.mention}  {action}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("me")