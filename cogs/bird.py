import discord, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def bird(self, ctx):
        animal_images = requests.get("https://some-random-api.ml/img/birb").json()
        async with ctx.typing():
            embed = discord.Embed(title="Un oiseau sauvage apparaît !", description="Cui-cui !")
            embed.set_image(url=animal_images['link'])
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("bird")