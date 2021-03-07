import discord, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):
        async with ctx.channel.typing():
            meme_response = requests.get("https://meme-api.herokuapp.com/gimme").json()
            embed = discord.Embed(title=f"Meme", description=meme_response["postLink"])
            embed.add_field(name=f"Meme de {meme_response['author']}", value=f"Subreddit : **r/{meme_response['subreddit']}** | <:reddit_upvote:791346828012552202> {meme_response['ups']}", inline=False)
            embed.set_image(url=meme_response['url'])
        await ctx.send(embed=embed)  

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("meme")