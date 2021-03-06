import discord, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def apod(self, ctx):
        async with ctx.channel.typing():
            apod_api_response = requests.get("https://api.nasa.gov/planetary/apod?api_key=Lre3As7v5IWN3OrJ4DuJCaGkhh3lvOA2dBdVWjef").json()
            embed = discord.Embed(title="Astronomy Picture Of the Day — APOD", color=0x00008b)
            embed.add_field(name=f"{apod_api_response['title']}", value="** **", inline=False)
            embed.set_image(url=apod_api_response["hdurl"])
            embed.set_footer(text=f"Type de média : {apod_api_response['media_type']}, si le type de média indique autre chose que 'image', alors c'est normal s'il n'y a pas de pièces jointes.")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("apod")