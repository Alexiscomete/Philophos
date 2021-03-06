import discord, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cat(self, ctx):
        animal_images = requests.get("http://aws.random.cat//meow").json()
        async with ctx.channel.typing():
            embed = discord.Embed(title="Un chat sauvage apparaît !", description="Meow !")
            embed.set_image(url=animal_images['file'])
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("cat")