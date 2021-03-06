import discord, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def dog(self, ctx):
        animal_images = requests.get("https://random.dog/woof.json").json()
        async with ctx.message.channel.typing():
            embed = discord.Embed(title="Un chien sauvage apparaît !", description="Woof !")
            embed.set_image(url=animal_images['url'])
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("dog")