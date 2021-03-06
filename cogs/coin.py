import discord, random, asyncio
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def coin(self, ctx):
        bot_message = await ctx.send("J'ai lancé la pièce.")
        await asyncio.sleep(1)
        if random.randint(1, 2) == 1:
            await bot_message.edit(content=f"{ctx.author.mention}, c'est pile !")
        else:
            await bot_message.edit(content=f"{ctx.author.mention}, c'est face !")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("coin")