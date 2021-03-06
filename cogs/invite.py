import discord
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def invite(self, ctx, *, arg):
        if arg == "server":
            await ctx.message.delete()
            await ctx.author.send("Voici le Discord du bot : https://discord.gg/WamZS7CExw (FR)")
        elif arg == "bot":
            await ctx.message.delete()
            await ctx.author.send("Pour m'inviter sur ton serveur Discord, utilise ce lien : <https://discord.com/oauth2/authorize?client_id=760171813866700850&permissions=134605888&scope=bot>")                
        else:
            await ctx.message.send(f"{ctx.author.mention} N'oublie pas l'argument ! (server ou bot)")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("invite")