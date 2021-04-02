import discord, requests, json
from discord.ext import commands
from discord_slash import cog_ext, SlashContext

class Slash(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @cog_ext.cog_slash(name="apod", description="Afficher la photo de la NASA du jour !")
    async def _apod(self, ctx):
        a_file = open("no-move.json", "r")
        json_object_nm = json.load(a_file)
        a_file.close()
        apod_api_key = json_object_nm['token']['apod']
        apod_api_response = requests.get(f"https://api.nasa.gov/planetary/apod?api_key={apod_api_key}").json()
        embed = discord.Embed(title="Astronomy Picture Of the Day — APOD", color=0x00008b)
        embed.add_field(name=f"{apod_api_response['title']}", value="** **", inline=False)
        embed.set_image(url=apod_api_response["hdurl"])
        embed.set_footer(text=f"Type de média : {apod_api_response['media_type']}, si le type de média indique autre chose que 'image', alors c'est normal s'il n'y a pas de pièces jointes.")
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(Slash(bot))

def teardown(bot):
    bot.remove_cog("apod")