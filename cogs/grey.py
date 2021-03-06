import discord, requests
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def grey(self, ctx):
        wasted = ctx.message.content.split(" ")
        async with ctx.typing():
            if len(wasted) > 1:
                try:
                    member = await self.client.fetch_user(str(wasted[1]).replace("<@",'').replace(">",'').replace("!",''))
                except discord.errors.HTTPException:
                    await ctx.send("L'identifiant entré n'est pas valide.")
                author_name = member.name
                author_mention = member.mention
                author_avatar_url = str(member.avatar_url)
            if len(wasted) == 1:
                author_name = ctx.author.name
                author_mention = ctx.author.mention
                author_avatar_url = ctx.author.avatar_url
            embed = discord.Embed(title=f":white_circle: {author_name} est gris·e !", description=author_mention)
            embed.set_image(url=f"https://some-random-api.ml/canvas/greyscale?avatar={str(author_avatar_url).replace('webp','png').replace('?size=1024','?size=4096')}")
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("grey")