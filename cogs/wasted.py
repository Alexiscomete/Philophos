import discord, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wasted(self, ctx, member: discord.Member = None):
        async with ctx.typing():
            if member != None:
                author_name = member.name
                author_mention = member.mention
                author_avatar_url = str(member.avatar_url)
            else:
                author_name = ctx.author.name
                author_mention = ctx.author.mention
                author_avatar_url = ctx.author.avatar_url
            embed = discord.Embed(title=f":thinking: {author_name} est recherché·e !", description=author_mention)
            embed.set_image(url=f"https://some-random-api.ml/canvas/wasted?avatar={str(author_avatar_url).replace('webp','png').replace('?size=1024','?size=4096')}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("wasted")