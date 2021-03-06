import discord, requests, urllib.request
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def triggered(self, ctx, member: discord.Member = None):
        async with ctx.typing():
            if member != None:
                author_name = member.name
                author_mention = member.mention
                author_avatar_url = str(member.avatar_url)
            else:
                author_name = ctx.author.name
                author_mention = ctx.author.mention
                author_avatar_url = str(ctx.author.avatar_url)
            avatar_url = urllib.request.urlretrieve(f"https://some-random-api.ml/canvas/triggered?avatar={str(author_avatar_url).replace('webp','png').replace('?size=1024','?size=4096')}", "images/triggered_profile_picture.gif")
            embed = discord.Embed(title=f":boom: {author_name} se secoue !", description=author_mention)
            file = discord.File("/root/discord-bots/AmanagerX/images/triggered_profile_picture.gif", filename="triggered_profile_picture.gif")
            embed.set_image(url="attachment://triggered_profile_picture.gif")
        await ctx.send(file=file, embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("triggered")