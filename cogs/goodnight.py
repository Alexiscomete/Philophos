import discord, TenGiphPy
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def goodnight(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
        goodnight_gif = rgif.random("goodnight anime")
        if member == None:
            embed.add_field(name=f"Bonne nuit {ctx.author.name} !", value=f'{ctx.author.mention}', inline=False)
            embed.set_image(url=goodnight_gif)
            await ctx.send(embed=embed)
        else:
            if str(member) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est dit bonne nuit !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=goodnight_gif)
                await ctx.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a dit bonne nuit à {member.name} !", value=f'{ctx.author.mention} {member.mention}', inline=False)
                embed.set_image(url=goodnight_gif)
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("goodnight")