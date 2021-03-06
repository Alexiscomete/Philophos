import discord, TenGiphPy
from discord.ext import commands
from datetime import date

class Others(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def halloween(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        today = date.today()
        d1 = today.strftime("%B %d, %Y")
        rgif = TenGiphPy.Tenor(token='88JQLKP3WXAI')
        halloween_gif = rgif.random("halloween")
        if "october" in d1.lower():
            embed = discord.Embed()
            if member == None:
                embed.add_field(name=f"** **", value=f"{ctx.author.mention} a eu peur... c'est Halloween !", inline=False)
                embed.set_image(url=halloween_gif)
                await ctx.send(embed=embed)
            else:
                if str(member) == str(ctx.author):
                    embed.add_field(name=f"** **", value=f"{ctx.author.mention} s'est fait peur à cause de son déguisement !?", inline=False)
                    embed.set_image(url=halloween_gif)
                    await ctx.send(embed=embed)
                else:
                    embed.add_field(name=f"** **", value=f'{ctx.author.mention} a fait peur à {member.mention} !', inline=False)
                    embed.set_image(url=halloween_gif)
                    await ctx.send(embed=embed)
        else:
            await ctx.send(f"{ctx.author.mention} C'est plus halloween, hein :wink:")

def setup(client):
    client.add_cog(Others(client))

def teardown(client):
    client.remove_cog("halloween")