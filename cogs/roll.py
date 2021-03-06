import discord, random, asyncio
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def roll(self, ctx):
        bot_message = await ctx.send("J'ai lancé le dé.")
        await asyncio.sleep(1/8)
        await bot_message.edit(content="J'ai lancé le dé..")
        await asyncio.sleep(1/8)
        await bot_message.edit(content="J'ai lancé le dé...")
        await asyncio.sleep(1/8)
        dice_face = random.randint(1, 6)
        await bot_message.edit(content=f"{ctx.author.mention}, c'est la face numéro **{dice_face}** !")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("roll")