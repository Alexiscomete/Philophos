import discord, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def redpanda(self, ctx):
        animal_images = requests.get("https://some-random-api.ml/img/red_panda").json()
        async with ctx.typing():
            embed = discord.Embed(title="Un panda roux sauvage apparaît !", description="Coo-coo !")
            embed.set_image(url=animal_images['link'])
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("panda")