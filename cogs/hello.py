import discord, TenGiphPy
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def hello(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
        hello_gif = rgif.random("hello anime")
        if member == None:
            embed.add_field(name=f"Salut {ctx.author.name} !", value=f'{ctx.author.mention}', inline=False)
            embed.set_image(url=hello_gif)
            await ctx.message.channel.send(embed=embed)
        else:
            if str(member) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est salué·e... !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=hello_gif)
                await ctx.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a salué {member.name} !", value=f'{ctx.author.mention} {member.mention}', inline=False)
                embed.set_image(url=hello_gif)
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("hello")