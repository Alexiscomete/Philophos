import discord
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def avatar(self, ctx):
        avatar = ctx.message.content.split(" ")
        if len(avatar) != 1:
            member = str(avatar[1]).replace("<@", "").replace(">", "").replace("!", "")
            try:
                member = await self.client.fetch_user(member)
            except:
                await ctx.send(f"La personne mentionnée n'a pas été retrouvée...")
            member_name = member.name
            member_mention = member.mention
            member_avatar = member.avatar_url
        else:
            member_name = ctx.author.name
            member_mention = ctx.author.mention
            member_avatar = ctx.author.avatar_url
        embed = discord.Embed(title=f"Avatar de {member_name}", description=member_mention)
        embed.set_image(url=member_avatar)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("avatar")