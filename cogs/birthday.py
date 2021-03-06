import discord, TenGiphPy
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def birthday(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
        birthday_gif = rgif.random("birthday anime")
        if member == None:
            embed.add_field(name=f"Bon anniversaire {ctx.author.name} !", value=f'{ctx.author.mention}', inline=False)
        else:
            if str(member) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est souhaité·e bon anniversaire !?", value=f"{ctx.author.mention}", inline=False)
            else:
                embed.add_field(name=f"{ctx.author.name} a souhaité un joyeux anniversaire à {member.name} !", value=f'{ctx.author.mention} {member.mention}', inline=False)
        embed.set_image(url=birthday_gif)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("birthday")