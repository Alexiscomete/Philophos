import discord
from discord.ext import commands
from discord.ext.commands import has_permissions

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def clear(self, ctx, clear: int = None):
        if ctx.author.guild_permissions.ban_members:
            if clear == None:
                await ctx.message.delete()
            else:
                await ctx.message.delete()
                await ctx.channel.purge(limit=clear)
        else:            
            await ctx.message.delete()
            await ctx.send(f"{ctx.author.mention} Tu n'as pas la permission de supprimer des messages.", delete_after=5)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("clear")