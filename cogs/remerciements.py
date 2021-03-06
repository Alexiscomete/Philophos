import discord
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def remerciements(self, ctx):
        await ctx.send(":heart: Merci à **Cyanic** de m'avoir beaucoup donné d'idées et à **Kobalt** d'être le traducteur de Polonais.\nMerci également à **Kyle / X Æ A-12**, **Cyanic**, **itai**, **Freeloop**, **LProgead** et **Kobalt** d'avoir été, et le sont toujours, les testeurs de ce bot !")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("remerciements")