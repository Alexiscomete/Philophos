import discord, TenGiphPy
from discord.ext import commands

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def pat(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        pat = ctx.message.content.split(" ")
        embed = discord.Embed()
        rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
        pat_gif = rgif.random("pat anime")
        if member == None:
            embed.add_field(name=f"{ctx.author.name} a été caressé·e !", value=f'{ctx.author.mention}', inline=False)
            embed.set_image(url=pat_gif)
            await ctx.send(embed=embed)
        else:
            if str(member) == str(ctx.author):
                embed.add_field(name=f"{ctx.author.name} s'est caressé·e !?", value=f"{ctx.author.mention}", inline=False)
                embed.set_image(url=pat_gif)
                await ctx.channel.send(embed=embed)
            else:
                embed.add_field(name=f"{ctx.author.name} a caressé {member.name} !", value=f'{ctx.author.mention} {member.mention}', inline=False)
                embed.set_image(url=pat_gif)
                await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("pat")