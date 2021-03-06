import discord, TenGiphPy
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def thank(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
        thanks_gif = rgif.random("thank anime")
        if member == None:
            embed.add_field(name=f"{ctx.author.name} a dit merci !", value=f"{ctx.author.mention}", inline=False)
            embed.set_image(url=thanks_gif)
            await ctx.send(embed=embed)
        else:
            if str(member) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est remercié !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=thanks_gif)
                await ctx.channel.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a remercié {member.name} !", value=f"{ctx.author.mention} {member.mention}", inline=False)
                embed.set_image(url=thanks_gif)
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("thank")