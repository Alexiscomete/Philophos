import discord, TenGiphPy
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def cookie(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        hello = ctx.message.content.split(" ")
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
        cookie_gif = rgif.random("anime cookie")
        if member == None:
            embed.add_field(name=f"{ctx.author.name} mange un cookie !", value=f'{ctx.author.mention}', inline=False)
        else:
            if str(member) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est donné un cookie... !?", value=f"{ctx.author.mention}", inline=False)
            else:
                embed.add_field(name=f"{ctx.author.name} a donné un cookie {member.name} !", value=f'{ctx.author.mention} {member.mention}', inline=False)
        embed.set_image(url=cookie_gif)
        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("cookie")