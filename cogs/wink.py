import discord, TenGiphPy
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def wink(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
        wink_gif = rgif.random("wink anime")
        if member == None:
            embed.add_field(name=f"{ctx.author.name} a fait un clin d'œil !", value=f"{ctx.author.mention}", inline=False)
            embed.set_image(url=wink_gif)
            await ctx.send(embed=embed)
        else:
            if str(member) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est fait un clin d'œil !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=wink_gif)
                await ctx.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a fait un clin d'œil à {member.name} !", value=f"{ctx.author.mention} {member.mention}", inline=False)
                embed.set_image(url=wink_gif)
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("wink")